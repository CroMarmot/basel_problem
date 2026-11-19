"""巴塞尔问题科普视频生成器

- 动画：Manim Community (v0.18+)
- 语音：Edge TTS 中文女声（英文成片换英文女声）
- 音视频合成：ffmpeg

运行：

    uv sync
    uv run ./basel_problem.py
    uv run ./basel_problem.py --list
    uv run ./basel_problem.py --chapters intro
    uv run ./basel_problem.py --segments geometry_light,geometry_circle
    uv run ./basel_problem.py --lang en      # 1:1 英文成片：旁白读 narration/en/，屏幕文字查 scenes/i18n.py

多屏章节（geometry、summary）按「一屏一个子片段」拆分，每段单独配音与合并，
再在章节内拼接，避免整章音视频内部不同步。

中间产物仍按原来的层级放在 `temp/chapters/` 下（英文成片放 `temp/chapters_en/`），只是文件名里带上内容指纹（xxhash）：
无声视频 = 场景源码（含它 import 的本地模块）+ 渲染参数 + 语言，音频 = 旁白文本 + TTS 参数，
merged = 两者联合，章节拼接 = 本章各 merged 联合。指纹没变就直接复用现成文件，同目录里
指纹过期的旧文件会被删掉；`temp/` 不再整体清空，想强制重来就 `rm -rf temp`。
"""

import argparse
import ast
import asyncio
import inspect
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import manim
import xxhash
from manim import config

from scenes import CHAPTER_NUMBERS, CHAPTERS, SCENES

config.disable_caching = False
config.save_last_frame = False
config.renderer = "cairo"

try:
    import edge_tts
except ImportError:
    raise ImportError("请安装 edge-tts: uv add 'edge-tts>=6.1.14'")

BASE_DIR = Path(__file__).parent.resolve()
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
config.media_dir = str(TEMP_DIR / "manim_media")
NARRATION_DIR = BASE_DIR / "narration"
SCENE_MAP = dict(SCENES)
SCENES_DIR = BASE_DIR / "scenes"

# 中文是默认语言，路径与音色沿用原来的写法；英文成片只是另一套参数。
VOICES = {"zh": "zh-CN-XiaoxiaoNeural", "en": "en-US-AriaNeural"}
TTS_RATES = {"zh": "+0%", "en": "+8%"}
TTS_VOLUME = "+0%"
TAIL_BEAT = 0.8
LANG = "zh"
SCRIPT_SEGMENTS: dict[str, str] = {}


def chapters_root() -> Path:
    """分章中间产物按语言分目录，中英两套缓存互不覆盖。"""
    return TEMP_DIR / ("chapters" if LANG == "zh" else f"chapters_{LANG}")


def set_lang(lang: str) -> None:
    """切换成片语言。场景在构造时才读 BASEL_LANG，所以必须在渲染前设好。"""
    global LANG, SCRIPT_SEGMENTS
    if lang not in VOICES:
        raise SystemExit(f"未知语言: {lang}（可选 {', '.join(VOICES)}）")
    LANG = lang
    os.environ["BASEL_LANG"] = lang
    SCRIPT_SEGMENTS = load_narration(lang)


def load_chapter_narration(chapter_key: str, lang: str) -> dict[str, str]:
    """读取 narration/<lang>/<chapter>.md，返回 {子片段 key: TTS 逐字原稿}。"""
    path = NARRATION_DIR / lang / f"{chapter_key}.md"
    if not path.exists():
        raise SystemExit(f"缺少语音原稿: {path}")

    text = path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^##\s+([A-Za-z0-9_-]+)\s*$", text, re.MULTILINE))
    if not headings:
        raise SystemExit(f"{path} 中没有任何 '## 子片段名'")

    segments: dict[str, str] = {}
    for index, heading in enumerate(headings):
        key = heading.group(1)
        block_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[heading.end() : block_end].strip()
        if not body:
            raise SystemExit(f"{path} 的 {key} 旁白为空")
        if key in segments:
            raise SystemExit(f"{path} 的 {key} 重复")
        segments[key] = body

    return segments


def load_narration(lang: str) -> dict[str, str]:
    """按章节汇总语音原稿，并与 scenes 里的章节/子片段做一致性校验。"""
    narration: dict[str, str] = {}
    for chapter_key, _, chapter_segments in CHAPTERS:
        chapter_text = load_chapter_narration(chapter_key, lang)
        unknown = [key for key in chapter_text if key not in chapter_segments]
        if unknown:
            raise SystemExit(
                f"narration/{lang}/{chapter_key}.md 多出未使用的子片段: {', '.join(unknown)}"
            )
        missing = [key for key in chapter_segments if key not in chapter_text]
        if missing:
            raise SystemExit(
                f"narration/{lang}/{chapter_key}.md 缺少旁白: {', '.join(missing)}"
            )
        narration.update(chapter_text)
    return narration


def digest(*chunks: object) -> str:
    """把若干输入串成一个 xxhash 指纹（每段之间补 0，避免拼接歧义）。"""
    hasher = xxhash.xxh64()
    for chunk in chunks:
        raw = chunk.encode("utf-8") if isinstance(chunk, str) else bytes(chunk)
        hasher.update(raw)
        hasher.update(b"\0")
    return hasher.hexdigest()


def local_imports(path: Path) -> list[str]:
    """列出某个场景文件从 scenes 包内部 import 的模块名。"""
    names = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.level:
            if node.module:
                names.append(node.module)
            names.extend(alias.name for alias in node.names)
    return names


def scene_source_files(scene_class: type) -> list[Path]:
    """场景渲染真正依赖的源文件：它自己，加上它（递归）import 的本地模块。"""
    start = Path(inspect.getfile(scene_class))
    pending, seen = [start], set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for name in local_imports(path):
            for candidate in (SCENES_DIR / f"{name}.py", SCENES_DIR / name / "__init__.py"):
                if candidate.exists():
                    pending.append(candidate)
    return sorted(seen)


def render_settings_tag() -> str:
    """影响无声视频的参数：Manim 版本、帧率、分辨率、背景色、屏幕文字的语言。

    中文是默认，指纹里留空——这样加英文支持不会把中文成片的缓存整体作废。
    """
    return "|".join(
        str(value)
        for value in (
            manim.__version__,
            config.frame_rate,
            config.pixel_width,
            config.pixel_height,
            config.background_color,
            "" if LANG == "zh" else LANG,
        )
    )


def video_fingerprint(segment_key: str) -> str:
    scene_class = SCENE_MAP[segment_key]
    parts = [render_settings_tag(), scene_class.__name__]
    i18n = SCENES_DIR / "i18n.py"
    for path in scene_source_files(scene_class):
        if LANG == "zh" and path == i18n:
            # 中文画面直接用手上的字符串，英文对译表改字不该作废中文缓存。
            continue
        parts.append(str(path.relative_to(BASE_DIR)))
        parts.append(path.read_text(encoding="utf-8"))
    return digest(*parts)


def audio_fingerprint(segment_key: str) -> str:
    return digest(LANG, VOICES[LANG], TTS_RATES[LANG], TTS_VOLUME, SCRIPT_SEGMENTS[segment_key])


def merged_fingerprint(segment_key: str, video_hash: str, audio_hash: str) -> str:
    # 带上留白时长：改 TAIL_BEAT 属于改合并策略，旧的 merged 必须作废。
    return digest(f"{segment_key}/merged", video_hash, audio_hash, f"{TAIL_BEAT:g}")


def ready(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def prune(directory: Path, pattern: str, keep: Path) -> None:
    """删掉同目录下指纹过期的旧产物，每种成品在目录里始终只留当前那一份。"""
    for stale in directory.glob(pattern):
        if stale != keep:
            stale.unlink()


async def synthesize_audio(segment_key: str, mp3_path: Path) -> None:
    """按当前语言为某个片段生成语音。"""
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"生成语音: {segment_key}")
    communicate = edge_tts.Communicate(
        text=SCRIPT_SEGMENTS[segment_key],
        voice=VOICES[LANG],
        rate=TTS_RATES[LANG],
        volume=TTS_VOLUME,
    )
    await communicate.save(str(mp3_path))


def get_duration(file_path: Path, media_type: str = "audio") -> float:
    """用 ffprobe 获取音视频时长（秒）。"""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"无法获取 {media_type} 时长 {file_path}: {e}")
        return 0.0


def merge_video_audio_with_ffmpeg(video_in: Path, audio_in: Path, video_out: Path) -> bool:
    """合并无声视频和语音：语音说完之后至少留 TAIL_BEAT 秒，不足就用最后一帧补齐。"""
    video_codec = "libx264"
    audio_codec = "aac"

    v_duration = get_duration(video_in)
    a_duration = get_duration(audio_in)

    if v_duration <= 0 or a_duration <= 0:
        print("无法取得时长，跳过合并")
        return False

    print(f"视频时长: {v_duration:.2f} 秒")
    print(f"音频时长: {a_duration:.2f} 秒")

    # 画面本来就比语音长的屏（排好的空镜）不动，只补不够呼吸的那几屏。
    pad = a_duration + TAIL_BEAT - v_duration
    if pad > 0:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_in),
            "-i",
            str(audio_in),
            "-filter_complex",
            (
                "[0:v]split[v1][v2];"
                "[v2]trim=start_frame=999999,setpts=N/FRAME_RATE/TB[blank];"
                "[v1][blank]concat=n=2:v=1:a=0[vid];"
                f"[vid]tpad=stop_mode=clone:stop_duration={pad:.3f}[finalv]"
            ),
            "-map",
            "[finalv]",
            "-map",
            "1:a",
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            "-vsync",
            "vfr",
            str(video_out),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_in),
            "-i",
            str(audio_in),
            "-af",
            "apad",
            "-shortest",
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            str(video_out),
        ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"合并完成: {video_out}")
        return True
    except subprocess.CalledProcessError:
        print("FFmpeg 执行失败")
        return False


def concatenate_videos(video_paths: list[Path], output_path: Path) -> None:
    """用 ffmpeg 拼接多个视频。"""
    list_file = TEMP_DIR / "concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for video_path in video_paths:
            f.write(f"file '{video_path.resolve()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-ar",
        "24000",
        "-ac",
        "1",
        "-af",
        "aresample=async=1:first_pts=0",
        "-avoid_negative_ts",
        "make_zero",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def chapter_dir_name(key: str) -> str:
    return f"{CHAPTER_NUMBERS[key]:03d}-{key}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成巴塞尔问题分章科普视频")
    parser.add_argument(
        "--chapters",
        help="只生成指定章节，逗号分隔，例如：intro,history,fourier",
    )
    parser.add_argument(
        "--segments",
        help="只生成指定子片段，逗号分隔，例如：fourier,geometry_circle",
    )
    parser.add_argument(
        "--lang",
        default="zh",
        choices=sorted(VOICES),
        help="成片语言：zh 中文（默认），en 英文 1:1 版",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出全部章节和子片段后退出",
    )
    return parser.parse_args()


async def render_segment(segment_key: str, segment_dir: Path) -> tuple[Path, str]:
    """渲染一个子片段，返回 (带音频的 merged.mp4, 它的指纹)。"""
    video_hash = video_fingerprint(segment_key)
    audio_hash = audio_fingerprint(segment_key)
    merge_hash = merged_fingerprint(segment_key, video_hash, audio_hash)

    silent_path = segment_dir / f"silent-{video_hash}.mp4"
    audio_path = segment_dir / f"{segment_key}-{audio_hash}.mp3"
    merged_path = segment_dir / f"merged-{merge_hash}.mp4"
    segment_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n处理片段: {segment_key}")
    if ready(merged_path):
        print(f"复用整段: {merged_path.name}")
    else:
        if ready(silent_path):
            print(f"复用无声视频: {silent_path.name}")
        else:
            scene = SCENE_MAP[segment_key]()
            scene.render()
            shutil.move(scene.renderer.file_writer.movie_file_path, silent_path)
            print(f"无声视频: {silent_path}")
        if ready(audio_path):
            print(f"复用语音: {audio_path.name}")
        else:
            await synthesize_audio(segment_key, audio_path)
            print(f"语音文件: {audio_path}")
        if not merge_video_audio_with_ffmpeg(silent_path, audio_path, merged_path):
            sys.exit(1)

    prune(segment_dir, "silent-*.mp4", silent_path)
    prune(segment_dir, f"{segment_key}-*.mp3", audio_path)
    prune(segment_dir, "merged-*.mp4", merged_path)
    return merged_path, merge_hash


async def main() -> None:
    args = parse_args()
    set_lang(args.lang)
    chapter_map = {key: (number, segments) for key, number, segments in CHAPTERS}

    if args.list:
        for chapter_key, number, segments in CHAPTERS:
            print(f"{number:03d}-{chapter_key}:")
            for segment_key in segments:
                print(f"  {segment_key}: {SCRIPT_SEGMENTS[segment_key]}")
        return

    if args.chapters and args.segments:
        raise SystemExit("--chapters 与 --segments 不能同时使用")

    if not shutil.which("ffmpeg"):
        print("未找到 ffmpeg，请先安装 ffmpeg")
        sys.exit(1)

    if args.segments:
        requested = [key.strip() for key in args.segments.split(",") if key.strip()]
        unknown = [key for key in requested if key not in SCENE_MAP]
        if unknown:
            raise SystemExit(
                f"未知子片段: {', '.join(unknown)}\n可用子片段: {', '.join(SCENE_MAP)}"
            )
        requested_set = set(requested)
        final_clips: list[Path] = []
        for chapter_key, _, segments in CHAPTERS:
            for index, segment_key in enumerate(segments, start=1):
                if segment_key not in requested_set:
                    continue
                segment_dir = (
                    chapters_root()
                    / chapter_dir_name(chapter_key)
                    / "segments"
                    / f"{index:02d}-{segment_key}"
                )
                clip, _ = await render_segment(segment_key, segment_dir)
                final_clips.append(clip)
        print("\n子片段已生成，未写入 output：")
        for clip in final_clips:
            print(f"  {clip}")
        return

    if args.chapters:
        requested = [key.strip() for key in args.chapters.split(",") if key.strip()]
        unknown = [key for key in requested if key not in chapter_map]
        if unknown:
            raise SystemExit(
                f"未知章节: {', '.join(unknown)}\n可用章节: {', '.join(chapter_map)}"
            )
        selected = [
            (chapter_key, segments)
            for chapter_key, _, segments in CHAPTERS
            if chapter_key in requested
        ]
    else:
        selected = [
            (chapter_key, segments) for chapter_key, _, segments in CHAPTERS
        ]

    final_clips: list[Path] = []
    for chapter_key, segments in selected:
        print(f"\n处理章节: {chapter_dir_name(chapter_key)}")
        chapter_dir = chapters_root() / chapter_dir_name(chapter_key)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        segment_clips: list[Path] = []
        segment_hashes: list[str] = []
        for index, segment_key in enumerate(segments, start=1):
            if len(segments) == 1 and segment_key == chapter_key:
                segment_dir = chapter_dir
            else:
                segment_dir = (
                    chapter_dir / "segments" / f"{index:02d}-{segment_key}"
                )
            clip, clip_hash = await render_segment(segment_key, segment_dir)
            segment_clips.append(clip)
            segment_hashes.append(clip_hash)

        if len(segment_clips) == 1:
            # 单屏章节不需要拼接，片段本身就是章节视频。
            chapter_clip = segment_clips[0]
        else:
            chapter_hash = digest(f"{chapter_key}/chapter", *segment_hashes)
            chapter_clip = chapter_dir / f"merged-{chapter_hash}.mp4"
            if ready(chapter_clip):
                print(f"复用章节拼接: {chapter_clip.name}")
            else:
                concatenate_videos(segment_clips, chapter_clip)
                print(f"章节合并完成: {chapter_clip}")
            prune(chapter_dir, "merged-*.mp4", chapter_clip)
        final_clips.append(chapter_clip)

    if args.chapters:
        print("\n章节已生成，未写入 output：")
        for clip in final_clips:
            print(f"  {clip}")
        return

    suffix = "" if LANG == "zh" else f"_{LANG}"
    final_output = OUTPUT_DIR / f"basel_problem_final{suffix}.mp4"
    concatenate_videos(final_clips, final_output)
    print(f"\n最终视频已生成: {final_output}")


if __name__ == "__main__":
    asyncio.run(main())
