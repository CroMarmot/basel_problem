# 巴塞尔问题项目规格（Spec）

> 这是项目的**前置描述文件**。`basel_problem.py` 会从「章节脚本」读取每章旁白，再调用 `scenes/` 中对应的章节渲染、配音、合并；`paper/` 下的论文也应与这里的设定保持一致。

## 目标

用一支约两分钟的中文科普视频和一篇四页左右的中文小论文，讲清楚：

1. 巴塞尔问题问的是什么；
2. 为什么这个级数收敛；
3. 欧拉如何得到 $\sum_{n=1}^{\infty} \frac{1}{n^2}=\frac{\pi^2}{6}$；
4. 傅里叶级数如何给出更严格的证明；
5. Wästlund 如何用欧几里得几何重新证明它。

## 受众与风格

- 受众：具备高中数学基础、对数学史和公式推导感兴趣的观众。
- 视频：节奏清晰，先提出问题，再给直觉，最后落到公式。
- 论文：比视频更完整，保留证明步骤和参考文献。
- 中文表达优先使用自然口语；公式中的变量和符号保持数学写法。
- 视觉：黑底白字；标题、正文默认白色，只用一种强调色（黄色）突出关键结论。
- 避免夸张音效和复杂转场，以排版、颜色和公式动画为主。

## 输出

- 最终视频：`output/basel_problem_final.mp4`，只在完整运行时生成。
- 单章测试：`temp/chapters/<三位编号>-<章节名>/merged.mp4`，不写入 `output/`。
- 论文：`output/basel_problem_paper.pdf`
- 中间产物：`temp/chapters/<三位编号>-<章节名>/silent.mp4`、`<章节名>.mp3`、`merged.mp4`
- Manim 缓存：`temp/manim_media/`

## 技术约束

- Python 3.12，Manim 0.22.x，Edge TTS，ffmpeg。
- 中文视频字体：`Noto Sans CJK SC`。
- 中文 PDF 使用 XeLaTeX + `fontspec` + Noto CJK 字体，不使用 `pdflatex`。
- PDF 构建后必须检查日志中是否出现 `Missing character`。
- 每次完整运行会清空 `temp/`，但不会删除 `output/`。
- `temp/chapters/` 下的目录使用三位数字前缀，保证文件管理器按章节顺序排序。
- `specs.md` 是旁白的唯一来源；修改旁白后重新运行视频脚本即可。

## 章节脚本

### intro

**旁白**

大家好！今天我们来聊聊巴塞尔问题。问题是：把所有正整数平方的倒数加起来，和是多少？

**画面**

整页只有三行：

1. 顶部标题「巴塞尔问题」，右侧附拉丁文「Basel Problem」；
2. 第二行问题描述「所有正整数平方的倒数之和是多少？」；
3. 第三行公式：

$$
S=\sum_{n=1}^{\infty}\frac{1}{n^2}
=1+\frac{1}{4}+\frac{1}{9}+\frac{1}{16}+\cdots=?
$$

不显示任何答案。

### history

**旁白**

这个问题在一六四四年由意大利数学家蒙戈利提出，后来因为伯努利兄弟的研究而广为人知。一七三五年，二十八岁的欧拉给出了答案：六分之派的平方。

**画面**

顶部标题为「从蒙戈利到欧拉」，下一行以小号拉丁字母标注「Basel Problem · Mengoli to Euler」。

标题下方左对齐依次显示四行：

1. 1644 年，蒙戈利（Pietro Mengoli）提出平方倒数和问题；
2. 伯努利兄弟（Jakob & Johann Bernoulli）研究但未能求出精确值；
3. 1735 年，欧拉（Leonhard Euler）得到 $\frac{\pi^2}{6}$，结果用黄色强调；
4. 欧拉因此声名大噪。

动画：标题写出后，四行内容从右侧依次淡入，最后停留约 3 秒。

### convergence

**旁白**

正项级数的收敛性，只需要简单的裂项就能证明。

**画面**

用一条多行长等式展示：

$$
\begin{aligned}
S&=\sum_{n=1}^{\infty}\frac{1}{n^2}
=1+\sum_{n=2}^{\infty}\frac{1}{n^2}\\
&<1+\sum_{n=2}^{\infty}\frac{1}{n(n-1)}
=1+\sum_{n=2}^{\infty}\left(\frac{1}{n-1}-\frac{1}{n}\right)\\
&=2.
\end{aligned}
$$

最后一步 $=2$ 用黄色强调，并说明因此级数收敛。

### euler

**旁白**

欧拉的想法非常大胆。他通过类比多项式的因式分解，猜出正弦函数除以 x 的无穷乘积。再把乘积展开，与泰勒展开比较平方项系数，就得到总和等于六分之派的平方。

**画面**

标题「欧拉的无穷乘积」，副标题「类比多项式的因式分解」。

用一条多行长等式展示：

$$
\begin{aligned}
1-\left(\sum_{n=1}^{\infty}\frac{1}{n^2\pi^2}\right)x^2+\cdots
&=\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)\\
&=\prod_{n=1}^{\infty}\left(1-\frac{x}{n\pi}\right)\left(1+\frac{x}{n\pi}\right)\\
&=\frac{\sin x}{x}\\
&=1-\frac{x^2}{6}+\frac{x^4}{120}-\cdots
\end{aligned}
$$

先写出整条等式，再高亮左右两端的 $x^2$ 系数，最后写出 $\sum 1/n^2=\pi^2/6$。

### fourier

**旁白**

用傅里叶级数和帕塞瓦尔等式，把函数 x 在负派到派上展开，同样得到六分之派的平方。

**画面**

标题为「傅里叶级数与帕塞瓦尔等式」，下一行英文为「Fourier Series · Parseval's Identity」。

画面等分为左右两半。左侧列出帕塞瓦尔等式，不证明，只写条件和完整形式：

$$
f(x)\sim\frac{a_0}{2}
+\sum_{n=1}^{\infty}\left(a_n\cos(nx)+b_n\sin(nx)\right),
$$

$$
\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)^2\,dx
=\frac{a_0^2}{2}
+\sum_{n=1}^{\infty}\left(a_n^2+b_n^2\right).
$$

条件是 $f$ 在 $[-\pi,\pi]$ 上平方可积。右侧只列四行：

1. $f(x)=x,\quad -\pi<x<\pi$；
2. $f(x)=x=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$；
3. $\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx=\sum_{n=1}^{\infty}\left(\frac{2}{n}\right)^2$；
4. $\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。

不再写出 $=4\sum 1/n^2$、积分值等中间计算。全画面只用白色，不使用强调色。

### geometry

**旁白**

3Blue1Brown 介绍过一个漂亮的几何证明，来自瑞典数学家约翰·韦斯特伦德二零一零年的论文《通过欧几里得几何求逆平方和》。核心是一道几何题：直角三角形斜边上的高，满足倒数平方关系。反复使用它，平方倒数和会变成圆上的长度。极限时得到奇数平方倒数和等于八分之派的平方。偶数项是总和的四分之一，所以总和等于六分之派的平方。

**画面**

左侧画直角三角形、斜边上的高与外接圆，展示反勾股定理：

$$
\frac{1}{h^2}=\frac{1}{a^2}+\frac{1}{b^2}.
$$

右侧先写出

$$
1+\frac{1}{9}+\frac{1}{25}+\cdots=\frac{\pi^2}{8},
$$

再利用偶数项之和为 $S/4$，得到

$$
S=\frac{4}{3}\cdot\frac{\pi^2}{8}=\frac{\pi^2}{6}.
$$

画面标注 Johan Wästlund, 2010，并点明 3Blue1Brown 的科普来源。

## 论文结构

1. 摘要：问题、答案与三种证明路线。
2. 问题的提出：巴塞尔问题的历史与意义。
3. 收敛性：与裂项级数比较。
4. 欧拉的正弦乘积证明：形式推导与二次项比较。
5. 傅里叶级数证明：正弦级数与帕塞瓦尔等式。
6. Wästlund 的几何证明：反勾股定理、重复构造与极限圆。
7. 结语：三种证明之间的联系。
8. 参考文献：Euler、Wästlund、3Blue1Brown、Apostol 等。

## 验收标准

- `uv run ./basel_problem.py` 能生成完整视频。
- `uv run ./basel_problem.py --chapters intro` 能只生成指定章节，并保留其他章节的中间产物。
- 章节局部生成的结果留在 `temp/chapters/`，`output/` 中不出现分章视频。
- `temp/chapters/001-intro/` 下能看到 `silent.mp4`、`intro.mp3`、`merged.mp4`。
- `uv run python paper/build.py` 能生成四页左右的中文 PDF，且日志无 `Missing character`。
- 视频与 PDF 中的中文、公式、数字均正常显示。
