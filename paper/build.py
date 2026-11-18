"""使用 XeLaTeX 编译中文 PDF 论文。

关键点：
- 使用 XeLaTeX，而不是 pdflatex；
- 使用 fontspec 直接加载 Noto CJK 字体；
- 设置 XeTeX 中文断行参数；
- 编译后检查日志中的 Missing character，避免中文静默变成空白/乱码。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = PAPER_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "output"
TEX_NAME = "basel_problem_paper.tex"
PDF_NAME = "basel_problem_paper.pdf"

REQUIRED_FONTS = [
    "Noto Serif CJK SC",
    "Noto Sans CJK SC",
]


def check_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(
            f"未找到 {name}。请安装：sudo apt install texlive-xetex fonts-noto-cjk"
        )


def check_fonts() -> None:
    for font in REQUIRED_FONTS:
        result = subprocess.run(
            ["fc-match", "-f", "%{family}", font],
            capture_output=True,
            text=True,
            check=False,
        )
        family = result.stdout.strip()
        if font not in family:
            raise SystemExit(
                f"未找到字体 {font}（fc-match 返回 {family!r}）。\n"
                "请安装：sudo apt install fonts-noto-cjk"
            )
    print("字体检查通过: " + ", ".join(REQUIRED_FONTS))


def compile_pdf() -> Path:
    check_tool("xelatex")
    check_fonts()

    cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        TEX_NAME,
    ]

    for round_no in (1, 2):
        print(f"XeLaTeX 第 {round_no} 次编译...")
        result = subprocess.run(
            cmd,
            cwd=PAPER_DIR,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(result.stdout[-4000:])
            print(result.stderr[-2000:])
            raise SystemExit(f"XeLaTeX 编译失败，退出码 {result.returncode}")

    log_path = PAPER_DIR / TEX_NAME.replace(".tex", ".log")
    log_text = log_path.read_text(encoding="utf-8", errors="replace")

    if "Missing character" in log_text:
        for line in log_text.splitlines():
            if "Missing character" in line:
                print(line)
        raise SystemExit(
            "检测到 Missing character。请确认已安装 Noto CJK 字体，"
            "并检查 tex 文件中是否使用了字体不支持的字符。"
        )

    overfull = log_text.count("Overfull \\hbox")
    if overfull:
        print(f"提示：存在 {overfull} 处 Overfull \\hbox，可检查排版宽度。")

    pdf_path = PAPER_DIR / PDF_NAME
    if not pdf_path.exists():
        raise SystemExit("编译结束但未找到 PDF 文件")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_pdf = OUTPUT_DIR / PDF_NAME
    shutil.copy2(pdf_path, output_pdf)
    print(f"PDF 已生成: {output_pdf}")
    return output_pdf


if __name__ == "__main__":
    try:
        compile_pdf()
    except KeyboardInterrupt:
        sys.exit(130)
