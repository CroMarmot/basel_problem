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

如果机器上没有 `uv`，直接用虚拟环境的解释器，效果相同：

```bash
.venv/bin/python ./basel_problem.py --chapters geometry
.venv/bin/python paper/build.py
```

## 常用命令

```bash
# 列出全部章节和子片段（含每段旁白），确认 key 拼写
uv run ./basel_problem.py --list

# 整片重建：清空 temp/，重渲所有章节，写入 output/basel_problem_final.mp4
uv run ./basel_problem.py

# 重建某一章：只覆盖该章的 temp 目录，不动其他章节，也不写 output/
uv run ./basel_problem.py --chapters geometry
uv run ./basel_problem.py --chapters intro,history,fourier

# 只重渲某一屏（改动画节拍时用这个，最快）
uv run ./basel_problem.py --segments geometry_circle

# 一次重渲几屏，逗号分隔
uv run ./basel_problem.py --segments fourier_series,fourier_parseval,fourier_result

# 重建论文 PDF（XeLaTeX 两遍 + 字体与 Missing character 检查）
uv run python paper/build.py
```

章节 key 与子片段 key 分别来自 `scenes/__init__.py` 的 `CHAPTERS` 和 `SCENES`：
每个章节对应一个语音原稿 `narration/zh/<章节 key>.md`，其中的 `## <key>` 小节必须与
该章节的子片段一一对应，缺或多都会直接报错退出；`specs.md` 的 `### <key>` 只规定画面。

## 产物目录

`specs.md` 是人与 AI 约定成品的章节规格，`narration/zh/` 是逐字语音原稿。视频会逐章渲染、配音、合并，再拼接成片。

中间产物保存在：

```text
temp/chapters/<三位编号>-<章节名>/
├── silent.mp4                 # 单片段章节
├── <章节名>.mp3
├── merged.mp4
└── segments/                  # 多片段章节
    └── <两位序号>-<片段名>/
        ├── silent.mp4
        ├── <片段名>.mp3
        └── merged.mp4
```

例如第一章是 `temp/chapters/001-intro/`，后面的 history 是 `002-history`。数字前缀保证 Ubuntu 文件管理器和各类 IDE 按章节顺序排序。傅里叶章 `005-fourier`、几何章 `006-geometry` 按画面拆成多个子片段，章节视频由片段依次拼接而成。只有 `intro` 这类章节 key 与子片段 key 相同时，产物才直接放在章节目录里；`007-summary` 的三屏仍然走 `segments/01-geometry_summary/`、`segments/02-geometry_question/`、`segments/03-geometry_direct/`。

只生成指定章节时，只会替换该章节目录，其他章节的中间产物会保留，结果留在 `temp/chapters/` 下，不写入 `output/`。完整运行会先清空 `temp/`，再重新生成全部章节并输出 `output/basel_problem_final.mp4`。`output/` 只保存最终视频和论文 PDF。

动画时长与旁白时长按片段补齐，因此每个片段只覆盖一屏内容，避免整章音画漂移。

## 改一屏的典型流程

```bash
# 1. 改动画：编辑 scenes/geometry.py 里对应的 Scene 类
# 2. 只重渲这一屏（终端会打印这一段的视频时长与音频时长）
uv run ./basel_problem.py --segments geometry_circle

# 3. 播一眼这一屏，人眼检查画面和配音是否对得上
xdg-open temp/chapters/006-geometry/segments/03-geometry_circle/merged.mp4

# 4. 满意后重建整章，章节视频由 6 个子片段依次拼接
uv run ./basel_problem.py --chapters geometry
```

旁白改在 `narration/zh/<章节 key>.md` 对应 `## <key>` 小节里的正文。`--segments` 会先删掉片段
目录，所以配音一定按新文字重新生成。排 `self.wait()` 时让动画总时长略大于旁白
（多 0.5～1 秒）：音频比视频长时，合并会把最后一帧冻住补满，看起来像卡带。

## 生成 PDF 论文

编译命令见上面的「常用命令」，`paper/build.py` 会检查字体、跑两遍 XeLaTeX，
并在日志出现 `Missing character` 时报错退出（中文静默变空白的常见来源）。

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
├── specs.md                  # 前置规格：目标、章节画面、论文结构
├── narration/
│   ├── README.md             # 语音原稿的写法与同音替字表
│   └── zh/                   # 中文逐字稿，一章一个文件（将来英文稿放 en/）
├── scenes/
│   ├── common.py             # 字体与强调色
│   ├── intro.py              # 001 巴塞尔问题
│   ├── history.py            # 002 从蒙戈利到欧拉
│   ├── convergence.py        # 003 收敛性
│   ├── euler.py              # 004 欧拉的无穷乘积
│   ├── fourier.py            # 005 傅里叶级数与帕塞瓦尔等式（3 屏）
│   ├── geometry.py           # 006 Wästlund 几何证明（6 屏）
│   └── summary.py            # 007 几何方法总结（3 屏）
├── paper/
│   ├── basel_problem_paper.tex
│   ├── build.py              # XeLaTeX 编译脚本
│   └── sections/             # 按章节拆分的论文正文
├── output/                   # 生成的视频与 PDF（忽略）
├── temp/                     # 分章中间产物与 Manim 缓存（忽略）
├── pyproject.toml
└── uv.lock
```
