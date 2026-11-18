"""巴塞尔问题科普视频生成器

- 动画：Manim Community (v0.18+)
- 语音：Edge TTS 中文女声
- 音视频合成：ffmpeg

运行：

    uv sync
    uv run ./basel_problem.py
    uv run ./basel_problem.py --list
    uv run ./basel_problem.py --chapters intro
    uv run ./basel_problem.py --segments geometry_light,geometry_circle

多屏章节（fourier、geometry）按「一屏一个子片段」拆分，每段单独配音与合并，
再在章节内拼接，避免整章音视频内部不同步。
"""

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

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
NARRATION_LANG = "zh"
SCENE_MAP = dict(SCENES)


def load_chapter_narration(chapter_key: str, lang: str = NARRATION_LANG) -> dict[str, str]:
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


def load_narration(lang: str = NARRATION_LANG) -> dict[str, str]:
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


SCRIPT_SEGMENTS = load_narration()


def reset_temp_dir() -> None:
    """每次完整运行前清空 temp，保证中间产物可重复生成。"""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)
    config.media_dir = str(TEMP_DIR / "manim_media")


async def generate_audio_segment(key: str, chapter_dir: Path) -> Path:
    """为某个片段生成中文语音，返回 MP3 路径。"""
    chapter_dir.mkdir(parents=True, exist_ok=True)
    text = SCRIPT_SEGMENTS[key]
    mp3_path = chapter_dir / f"{key}.mp3"
    if not mp3_path.exists():
        print(f"生成语音: {key}")
        communicate = edge_tts.Communicate(
            text=text,
            voice="zh-CN-XiaoxiaoNeural",
            rate="+0%",
            volume="+0%",
        )
        await communicate.save(str(mp3_path))
    return mp3_path


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
    """按较长的一路补齐另一路，合并无声视频和语音。"""
    video_codec = "libx264"
    audio_codec = "aac"

    v_duration = get_duration(video_in)
    a_duration = get_duration(audio_in)

    if v_duration <= 0 or a_duration <= 0:
        print("无法取得时长，跳过合并")
        return False

    print(f"视频时长: {v_duration:.2f} 秒")
    print(f"音频时长: {a_duration:.2f} 秒")

    if a_duration > v_duration:
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
                "[vid]tpad=stop_mode=clone:stop_duration=1000000[finalv]"
            ),
            "-map",
            "[finalv]",
            "-map",
            "1:a",
            "-shortest",
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
        help="只生成指定子片段，逗号分隔，例如：fourier_series,fourier_result",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出全部章节和子片段后退出",
    )
    return parser.parse_args()


async def render_segment(segment_key: str, segment_dir: Path) -> Path:
    """渲染一个子片段，返回带音频的 merged.mp4。"""
    segment_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n处理片段: {segment_key}")

    video_path = segment_dir / "silent.mp4"
    scene = SCENE_MAP[segment_key]()
    scene.render()
    rendered = scene.renderer.file_writer.movie_file_path
    shutil.move(rendered, video_path)
    print(f"无声视频: {video_path}")

    audio_path = await generate_audio_segment(segment_key, segment_dir)
    print(f"语音文件: {audio_path}")

    merged_path = segment_dir / "merged.mp4"
    if not merge_video_audio_with_ffmpeg(video_path, audio_path, merged_path):
        sys.exit(1)
    return merged_path


async def main() -> None:
    args = parse_args()
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
        TEMP_DIR.mkdir(exist_ok=True)
        final_clips: list[Path] = []
        for chapter_key, _, segments in CHAPTERS:
            for index, segment_key in enumerate(segments, start=1):
                if segment_key not in requested_set:
                    continue
                segment_dir = (
                    TEMP_DIR
                    / "chapters"
                    / chapter_dir_name(chapter_key)
                    / "segments"
                    / f"{index:02d}-{segment_key}"
                )
                shutil.rmtree(segment_dir, ignore_errors=True)
                final_clips.append(await render_segment(segment_key, segment_dir))
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
        TEMP_DIR.mkdir(exist_ok=True)
    else:
        selected = [
            (chapter_key, segments) for chapter_key, _, segments in CHAPTERS
        ]
        reset_temp_dir()

    final_clips: list[Path] = []
    for chapter_key, segments in selected:
        print(f"\n处理章节: {chapter_dir_name(chapter_key)}")
        chapter_dir = TEMP_DIR / "chapters" / chapter_dir_name(chapter_key)
        shutil.rmtree(chapter_dir, ignore_errors=True)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        segment_clips: list[Path] = []
        for index, segment_key in enumerate(segments, start=1):
            if len(segments) == 1 and segment_key == chapter_key:
                segment_dir = chapter_dir
            else:
                segment_dir = (
                    chapter_dir / "segments" / f"{index:02d}-{segment_key}"
                )
            segment_clips.append(await render_segment(segment_key, segment_dir))

        if len(segment_clips) == 1:
            chapter_clip = segment_clips[0]
        else:
            chapter_clip = chapter_dir / "merged.mp4"
            concatenate_videos(segment_clips, chapter_clip)
            print(f"章节合并完成: {chapter_clip}")
        final_clips.append(chapter_clip)

    if args.chapters:
        print("\n章节已生成，未写入 output：")
        for clip in final_clips:
            print(f"  {clip}")
        return

    final_output = OUTPUT_DIR / "basel_problem_final.mp4"
    concatenate_videos(final_clips, final_output)
    print(f"\n最终视频已生成: {final_output}")


if __name__ == "__main__":
    asyncio.run(main())
