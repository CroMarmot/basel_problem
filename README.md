# basel-problem

用 Manim + Edge TTS 生成“巴塞尔问题”科普视频（中文为主，另有逐句对译的英文版），并用 XeLaTeX 生成中文 PDF 论文、pdfLaTeX 生成英文版（arXiv）。

## 快速开始

```bash
# 需要 ffmpeg 完成音视频合并
# sudo apt install ffmpeg
uv sync
uv run ./basel_problem.py          # 中文版
uv run ./basel_problem.py --lang en  # 英文版（1:1 对译，另需联网配音）
```

最终视频输出到：

```text
output/basel_problem_final.mp4
output/basel_problem_final_en.mp4
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
uv run ./basel_problem.py --segments fourier,geometry_circle

# 英文版：所有 key 与中文一致，只是产物放 temp/chapters_en/、换成英文旁白与英文屏幕字
uv run ./basel_problem.py --lang en --chapters geometry
uv run ./basel_problem.py --lang en --segments geometry_circle

# 重建论文 PDF（XeLaTeX 两遍 + 字体与 Missing character 检查）
uv run python paper/build.py

# 中文几何版（只讲 Wästlund + 补灯一步，与英文版逐节对应）
uv run python paper_geo/build.py

# 重建英文版论文 PDF（pdfLaTeX 两遍，arXiv 用）
uv run python paper_en/build.py
```

章节 key 与子片段 key 分别来自 `scenes/__init__.py` 的 `CHAPTERS` 和 `SCENES`：
- 每个章节对应一个语音原稿 `narration/<lang>/<章节 key>.md`，其中的 `## <key>` 小节必须与该章节的子片段一一对应，缺或多都会直接报错退出；`specs.md` 的 `### <key>` 只规定画面。
- 英文版 `narration/en/` 是中文稿的 1:1 对译，同音替字（药求、鸡数、派、倒树）只存在于中文稿里。
- 屏幕上的中文字由 `scenes/i18n.py` 整表对译：`--lang en` 时 `cn()` 与 `screen_title` 查这张表，
- 表里缺一条就直接报错退出，所以英文版不会漏出中文；中文副标题若只是主标题的英文翻译，在表里置为 `None` 即可去掉。

## 产物目录

`specs.md` 是人与 AI 约定成品的章节规格，`narration/zh/` 与 `narration/en/` 是逐字语音原稿。视频会逐章渲染、配音、合并，再拼接成片。

中间产物都保存在 `temp/` 里，层级和以前一样，只是文件名里插入了内容指纹（xxhash）：

```text
temp/
├── manim_media/
├── chapters/<三位编号>-<章节名>/             # 中文版
└── chapters_en/<三位编号>-<章节名>/          # 英文版，层级完全相同
    ├── silent-<vhash>.mp4              # 单片段章节
    ├── <章节名>-<ahash>.mp3
    ├── merged-<mhash>.mp4
    ├── merged-<chash>.mp4              # 多片段章节的拼接成品
    └── segments/
        └── <两位序号>-<片段名>/
            ├── silent-<vhash>.mp4      # hash(场景源码 + 它 import 的本地模块, Manim 版本, 帧率, 分辨率, 背景色, 屏幕文字语言)
            ├── <片段名>-<ahash>.mp3    # hash(语言, 音色, rate, volume, 旁白文本)
            └── merged-<mhash>.mp4      # hash(vhash + ahash + TAIL_BEAT)
```

音视频按片段合并：语音说完之后至少留 `TAIL_BEAT = 0.8` 秒，画面不够长就用**最后一帧定格**补齐；
本来就比语音长的空镜不动。因此**每屏结尾不能淡出到黑**，否则英文版超时的语音会冻在一张黑图上
（006 的五屏原本以 `FadeOut(everything)` 收尾，现已换成等长的 `self.wait(0.5)`）。

## 生成 PDF 论文

编译命令见上面的「常用命令」，`paper/build.py` 会检查字体、跑两遍 XeLaTeX，
并在日志出现 `Missing character` 时报错退出（中文静默变空白的常见来源）。

最终 PDF 输出到：

```text
output/basel_problem_paper.pdf       # 中文版（与视频一致：三条路线）
output/basel_problem_paper_geo.pdf   # 中文几何版（与英文版逐节对应）
output/basel_problem_paper_en.pdf    # 英文版（arXiv）
```

英文版走 `paper_en/build.py`，用 **pdfLaTeX** 而不是 XeLaTeX：arXiv 的 TeXLive 没有 Noto CJK，中文源码原样上传会构建失败，所以英文版只收几何路线（Wästlund 的证明 + 本文的补灯一步），全篇 ASCII 加 `\` 转音号（`W\"astlund`）。检查项换成未定义引用/引文与缺字。

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
│   ├── zh/                   # 中文逐字稿，一章一个文件
│   └── en/                   # 英文逐字稿，与 zh/ 一一对应
├── scenes/
│   ├── common.py             # 字体、强调色，以及按语言取屏幕字的 cn()/screen_title
│   ├── i18n.py               # 屏幕中文 → 英文的对译表（缺条目就报错）
│   ├── intro.py              # 001 巴塞尔问题
│   ├── history.py            # 002 从蒙戈利到欧拉
│   ├── convergence.py        # 003 收敛性
│   ├── euler.py              # 004 欧拉的无穷乘积
│   ├── fourier.py            # 005 傅里叶级数与帕塞瓦尔等式（1 屏）
│   ├── geometry.py           # 006 Wästlund 几何证明（6 屏）
│   └── summary.py            # 007 几何方法总结（5 屏，末屏是参考链接）
├── paper/
│   ├── basel_problem_paper.tex
│   ├── build.py              # XeLaTeX 编译脚本
│   └── sections/             # 按章节拆分的论文正文
├── paper_geo/
│   ├── basel_problem_paper_geo.tex
│   ├── build.py              # XeLaTeX 编译脚本（中文几何版）
│   └── sections/             # 与 paper_en/ 逐节对应的中文正文
├── paper_en/
│   ├── basel_problem_paper_en.tex
│   ├── build.py              # pdfLaTeX 编译脚本（arXiv 可用）
│   └── sections/             # 英文版正文，只有几何路线
├── docs/                     # 制作过程的对话记录存档（不参与构建）
├── output/                   # 生成的视频与 PDF（忽略）
├── temp/                     # 分章中间产物与 Manim 缓存（忽略）
├── pyproject.toml
└── uv.lock
```

## 关于制作过程

动画脚本、画面代码与三版论文的排版改写是在 AI 编程助手的协助下完成的，主要对话记录存档在
`docs/qwen3.8_flash_part_source_code.md`。数学内容——构造、证明与结论——由作者本人负责。
