# basel-problem

用 Manim + Edge TTS 生成“巴塞尔问题”科普视频，并用 XeLaTeX 生成中文 PDF 论文。

## 快速开始

```bash
# 需要 ffmpeg 完成音视频合并
# sudo apt install ffmpeg
uv sync
uv run ./basel_problem.py
```

最终视频输出到：

```text
output/basel_problem_final.mp4
```

## 分章生成

`specs.md` 是前置的章节规格与旁白来源。视频会逐章渲染、配音、合并，再拼接成片。

```bash
# 查看章节
uv run ./basel_problem.py --list

# 只生成第一章，结果在 temp/chapters/001-intro/merged.mp4
uv run ./basel_problem.py --chapters intro
```

中间产物保存在：

```text
temp/chapters/<三位编号>-<章节名>/
├── silent.mp4
├── <章节名>.mp3
└── merged.mp4
```

例如第一章是 `temp/chapters/001-intro/`，后面的 history 是 `002-history`。数字前缀保证 Ubuntu 文件管理器和各类 IDE 按章节顺序排序。

只生成指定章节时，只会替换该章节目录，其他章节的中间产物会保留，结果留在 `temp/chapters/` 下，不写入 `output/`。完整运行会先清空 `temp/`，再重新生成全部章节并输出 `output/basel_problem_final.mp4`。`output/` 只保存最终视频和论文 PDF。

## 生成 PDF 论文

```bash
uv run python paper/build.py
```

最终 PDF 输出到：

```text
output/basel_problem_paper.pdf
```

### 中文 PDF 乱码问题

本项目使用 **XeLaTeX + fontspec + Noto CJK 字体**，并显式设置：

```tex
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt
```

因此不要用 `pdflatex` 编译中文文档，也不要依赖缺失的 `ctex`/`xeCJK` 包。

如果系统缺少字体或 XeLaTeX，安装：

```bash
sudo apt install texlive-xetex fonts-noto-cjk
```

## 目录结构

```text
basel-problem/
├── basel_problem.py          # 入口：参数、TTS、音视频合并与拼接
├── specs.md                  # 前置规格：目标、章节旁白、论文结构
├── scenes/
│   ├── common.py             # 字体与强调色
│   ├── intro.py              # 001 巴塞尔问题
│   ├── history.py            # 002 从蒙戈利到欧拉
│   ├── convergence.py        # 003 收敛性
│   ├── euler.py              # 004 欧拉的无穷乘积
│   ├── fourier.py            # 005 傅里叶级数与帕塞瓦尔等式
│   └── geometry.py           # 007 Wästlund 几何证明
├── paper/
│   ├── basel_problem_paper.tex
│   ├── build.py              # XeLaTeX 编译脚本
│   └── sections/             # 按章节拆分的论文正文
├── output/                   # 生成的视频与 PDF（忽略）
├── temp/                     # 分章中间产物与 Manim 缓存（忽略）
├── pyproject.toml
└── uv.lock
```
