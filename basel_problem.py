"""巴塞尔问题科普视频生成器

- 动画：Manim Community (v0.18+)
- 语音：Edge TTS 中文女声
- 音视频合成：ffmpeg

运行：

    uv sync
    uv run ./basel_problem.py
    uv run ./basel_problem.py --list
    uv run ./basel_problem.py --chapters intro
"""

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

from manim import config

from scenes import CHAPTER_NUMBERS, SCENES

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
SPEC_PATH = BASE_DIR / "specs.md"


def load_script_segments(spec_path: Path) -> dict[str, str]:
    """从 specs.md 的「章节脚本」段落读取每章旁白。"""
    if not spec_path.exists():
        raise SystemExit(f"缺少章节脚本规格文件: {spec_path}")

    text = spec_path.read_text(encoding="utf-8")
    section_match = re.search(r"^##\s+章节脚本\s*$", text, re.MULTILINE)
    if section_match is None:
        raise SystemExit("specs.md 中缺少 '## 章节脚本' 段落")

    section = text[section_match.end() :]
    next_h2 = re.search(r"^##\s+", section, re.MULTILINE)
    if next_h2 is not None:
        section = section[: next_h2.start()]

    headings = list(re.finditer(r"^###\s+([A-Za-z0-9_-]+)\s*$", section, re.MULTILINE))
    if not headings:
        raise SystemExit("specs.md 的「章节脚本」中没有任何 '### 章节名'")

    segments: dict[str, str] = {}
    for index, heading in enumerate(headings):
        key = heading.group(1)
        block_end = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        block = section[heading.end() : block_end]

        narration_match = re.search(r"^\*\*旁白\*\*\s*$", block, re.MULTILINE)
        if narration_match is None:
            raise SystemExit(f"章节 {key} 缺少 '**旁白**' 段落")

        narration = block[narration_match.end() :]
        next_label = re.search(r"^\*\*[^*]+\*\*\s*$", narration, re.MULTILINE)
        if next_label is not None:
            narration = narration[: next_label.start()]

        narration = narration.strip()
        if not narration:
            raise SystemExit(f"章节 {key} 的旁白为空")
        segments[key] = narration

    return segments


SCRIPT_SEGMENTS = load_script_segments(SPEC_PATH)


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
        help="只生成指定章节，逗号分隔，例如：intro,history",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出全部章节后退出",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    scene_map = dict(SCENES)

    missing = [key for key, _ in SCENES if key not in SCRIPT_SEGMENTS]
    unused = [key for key in SCRIPT_SEGMENTS if key not in scene_map]
    if missing or unused:
        details = []
        if missing:
            details.append(f"specs.md 缺少旁白: {', '.join(missing)}")
        if unused:
            details.append(f"specs.md 多出未使用章节: {', '.join(unused)}")
        raise SystemExit("\n".join(details))

    if args.list:
        for key, _ in SCENES:
            print(f"{chapter_dir_name(key)}: {SCRIPT_SEGMENTS[key]}")
        return

    if args.chapters:
        requested = [key.strip() for key in args.chapters.split(",") if key.strip()]
        unknown = [key for key in requested if key not in scene_map]
        if unknown:
            raise SystemExit(
                f"未知章节: {', '.join(unknown)}\n可用章节: {', '.join(scene_map)}"
            )
        selected = [(key, scene_map[key]) for key in requested]
    else:
        selected = SCENES

    if not shutil.which("ffmpeg"):
        print("未找到 ffmpeg，请先安装 ffmpeg")
        sys.exit(1)

    if args.chapters:
        TEMP_DIR.mkdir(exist_ok=True)
    else:
        reset_temp_dir()
    final_clips: list[Path] = []

    for key, scene_class in selected:
        print(f"\n处理片段: {chapter_dir_name(key)}")

        chapter_dir = TEMP_DIR / "chapters" / chapter_dir_name(key)
        shutil.rmtree(chapter_dir, ignore_errors=True)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        video_path = chapter_dir / "silent.mp4"
        scene = scene_class()
        scene.render()
        rendered = scene.renderer.file_writer.movie_file_path
        shutil.move(rendered, video_path)
        print(f"无声视频: {video_path}")

        audio_path = await generate_audio_segment(key, chapter_dir)
        print(f"语音文件: {audio_path}")

        merged_path = chapter_dir / "merged.mp4"
        if not merge_video_audio_with_ffmpeg(video_path, audio_path, merged_path):
            sys.exit(1)
        final_clips.append(merged_path)

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
