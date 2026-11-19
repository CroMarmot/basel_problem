"""使用 pdfLaTeX 编译英文 PDF 论文（arXiv 提交版）。

关键点：
- 用 pdfLaTeX，不加载 fontspec/XeLaTeX 相关的中文设置；arXiv 的 TeXLive 没有 Noto CJK，
  英文版必须能在 pdfLaTeX 下构建；
- 编译两遍（交叉引用与页数）；
- 检查日志里的未定义引用/引文与 Missing character，避免 ? 和空白静默进入成品。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = PAPER_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "output"
TEX_NAME = "basel_problem_paper_en.tex"
PDF_NAME = "basel_problem_paper_en.pdf"


def check_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"未找到 {name}。请安装：sudo apt install texlive-latex-extra")


def run_pdflatex() -> None:
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        TEX_NAME,
    ]
    for round_no in (1, 2):
        print(f"pdfLaTeX 第 {round_no} 次编译...")
        result = subprocess.run(
            cmd, cwd=PAPER_DIR, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            print(result.stdout[-4000:])
            print(result.stderr[-2000:])
            raise SystemExit(f"pdfLaTeX 编译失败，退出码 {result.returncode}")


def check_log() -> None:
    log_text = (PAPER_DIR / TEX_NAME.replace(".tex", ".log")).read_text(
        encoding="utf-8", errors="replace"
    )
    problems = [
        line
        for line in log_text.splitlines()
        if "Missing character" in line
        or "There were undefined references" in line
        or "undefined citations" in line.lower()
        or "Citation" in line and "undefined" in line
    ]
    for line in problems:
        print(line)
    if problems:
        raise SystemExit("日志中存在未定义引用或缺字，请修复后再看 PDF")

    overfull = log_text.count("Overfull \\hbox")
    if overfull:
        print(f"提示：存在 {overfull} 处 Overfull \\hbox，可检查排版宽度。")


def copy_pdf() -> Path:
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
        check_tool("pdflatex")
        run_pdflatex()
        check_log()
        copy_pdf()
    except KeyboardInterrupt:
        sys.exit(130)
