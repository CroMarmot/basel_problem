"""屏幕文字的英文对译表。

只在 `BASEL_LANG=en` 时生效（见 `scenes/common.py`）。中文成片照旧直接用场景里的原句，
所以这张表是**单向覆盖**：英文缺哪一句，构建就直接失败，而不是把中文混进英文成片。

键是场景里出现的**完整原句**，逐字照抄。句末的全角标点可以省着写：
`"在 Wästlund 的几何图上再多走一步" + "？"` 会先整句查表，查不到再剥掉句末标点回查，
所以场景里用拼接出来的标题不必在表里重复登记。

值为 `None` 表示这一小块英文里不出现（例如「观察汇聚于 O₂ 的角」里的「的角」，
英文把语序并进了前一块）。
"""

# 句末全角标点 → 半角。剥掉后再回查一次表，用来支持 `标题 + "？"` 这类拼接。
TRAILING_PUNCT = {"？": "?", "！": "!", "：": ":", "，": ",", "、": ",", "。": "."}

TEXTS = {
    # ---- 001 intro ----
    "巴塞尔问题": "The Basel Problem",
    "所有正整数平方的倒数之和是多少？": (
        "What is the sum of the reciprocals of the squares of all positive integers?"
    ),
    # ---- 002 history ----
    "从蒙戈利到欧拉": "From Mengoli to Euler",
    "1735 年，欧拉（Leonhard Euler）得到": "In 1735, Euler obtained",
    "1644 年，蒙戈利（Pietro Mengoli）提出平方倒数和问题": (
        "In 1644 Pietro Mengoli posed the problem of the sum of reciprocal squares"
    ),
    "伯努利兄弟（Jakob & Johann Bernoulli）研究但未能求出精确值": (
        "The Bernoulli brothers studied it but never found the exact value"
    ),
    "欧拉因此声名大噪": "and Euler made his name with it",
    # ---- 003 convergence ----
    "收敛性": "Convergence",
    # ---- 004 euler ----
    "欧拉的无穷乘积": "Euler's infinite product",
    "类比多项式的因式分解": "By analogy with factoring polynomials",
    # ---- 005 fourier ----
    "傅里叶级数与帕塞瓦尔等式": "Fourier Series and Parseval's Identity",
    "帕塞瓦尔等式": "Parseval's identity",
    "条件：f 在 [−π, π] 上平方可积": "Condition: f is square integrable on [-pi, pi]",
    "函数平方的积分 = 系数平方之和": "integral of f² = sum of coefficients²",
    # ---- 006 geometry ----
    "Wästlund 的几何证明": "Wästlund's Geometric Proof",
    "平方反比看成接受光照": "The inverse square law read as light",
    "距离 d": "distance d",
    "面积 A": "area A",
    "亮度 B": "brightness B",
    "距离 2d": "distance 2d",
    "面积 4A": "area 4A",
    "亮度 B/4": "brightness B/4",
    "距离翻倍，亮度只剩四分之一": "Twice as far, a quarter as bright",
    "反勾股定理": "The inverse Pythagorean theorem",
    "面积法：ab = ch，再用 c² = a² + b²": "By areas: ab = ch, then c² = a² + b²",
    "一盏灯换成两盏等效灯": "One lamp becomes two equivalent lamps",
    "大圆半径是小圆的两倍": "the large radius is twice the small one",
    "PR 垂直于 S1S2": "PR is perpendicular to S1S2",
    "小圆上一盏灯的亮度 = 大圆上两盏灯的等效亮度": "one lamp = two equivalent lamps",
    "半径翻倍：N 等分换成 2N 等分": "Doubling the radius: N divisions become 2N",
    # 006-04 右侧那一列居中在 x=3，英文行宽要压到 7 个单位以内才不出画。
    "观察汇聚于": "Angles seen from",
    "的角": None,
    "对于小圆来说，圆周角两两相等": "small circle: equal inscribed angles",
    "对于大圆来说，圆心角两两相等": "large circle: equal central angles",
    "小圆的 N 等分点 = 大圆上": "N divisions become the",
    "「对应的」": "matching",
    "2N 等分点": "2N divisions",
    "极限：圆变成直线": "The limit: the circle becomes a line",
    "初始：周长 2，灯在 P 的正对面": "Start: circumference 2, lamp opposite P",
    "总亮度：": "Total brightness:",
    "回到巴塞尔问题": "Back to the Basel problem",
    # ---- 007 summary ----
    "在 Wästlund 的几何图上再多走一步": "One More Step on Wästlund's Geometric Picture",
    "① 三维点光源用面受光，亮度与距离平方成反比": (
        "① Light from a point source: brightness falls off as the square of the distance"
    ),
    "② 反勾股定理：一盏灯换成两盏等效灯": (
        "② Inverse Pythagorean theorem: one lamp becomes two equivalent lamps"
    ),
    "③ 半径倍增与等效替换，极限下得到奇数项之和": (
        "③ Double the radius, keep the equivalence; in the limit, the odd terms"
    ),
    "④ 代数运算得到最初要求的表达式": "④ A little algebra gives the expression we wanted",
    "几何方法的四步总结": "The geometric route in four steps",
    "能搜到的几何讲解，都是先求奇数项平方倒数和，\n再用代数算出 S": (
        "Every geometric explainer you can find stops at the odd terms,\nthen recovers S by algebra"
    ),
    "一个没被回答的问题": "A question nobody answered",
    "网上能搜到的二次讲解，和 3Blue1Brown 那期完全一样": (
        "Every follow-up online repeats the 3Blue1Brown video exactly"
    ),
    "不能直接从几何得到吗？": "Can't geometry hand it over directly?",
    # 007-02 是一条横排的四段链，标签必须比中文更紧凑，否则整行出画。
    "几何：圆与灯": "Circles and lamps",
    "几何得到": "from geometry",
    "代数收尾": "then algebra",
    "要求的表达式": "the target sum",
    "每翻一倍，只在正对面补一盏": "Each doubling: add one lamp, only at the far side",
    "每盏新灯给总亮度加上": "Each new lamp adds to the total brightness",
    # 007-04 左上角那条周长大字是场景里算出来的（2 的幂），只能逐个登记。
    "周长：2": "Circumference: 2",
    "周长：4": "Circumference: 4",
    "周长：8": "Circumference: 8",
    "周长：16": "Circumference: 16",
    "周长：32": "Circumference: 32",
    "两侧合起来的总亮度": "The brightness of both sides together",
    "一张图讲完整个证明": "One picture, the whole proof",
    "参考链接": "References",
    "几何证明原文": "the original geometric proof",
    "科普讲解视频": "the popular explainer video",
}


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def translate(text: str) -> str | None:
    """英文成片里这句话显示什么；`None` 表示这块文字不出现。"""
    if not has_cjk(text):
        return text
    if text in TEXTS:
        return TEXTS[text]
    last = text[-1] if text else ""
    if last in TRAILING_PUNCT and text[:-1] in TEXTS:
        tail = TEXTS[text[:-1]]
        return None if tail is None else tail + TRAILING_PUNCT[last]
    raise SystemExit(f"scenes/i18n.py 里缺少英文对译: {text!r}")
