from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    Indicate,
    Line,
    MathTex,
    Scene,
    Text,
    VGroup,
    Write,
)

from .common import CN_FONT


def cn(text: str, scale: float = 0.55) -> Text:
    return Text(text, font=CN_FONT).scale(scale)


def heading(title_text: str, subtitle_text: str) -> VGroup:
    title = cn(title_text, 0.85)
    title.to_edge(UP, buff=0.45)
    subtitle = Text(subtitle_text, font_size=22).scale(0.42)
    subtitle.next_to(title, DOWN, buff=0.1)
    return VGroup(title, subtitle)


class BaselFourier(Scene):
    """一屏讲完：左栏是帕塞瓦尔等式，右栏同一行写出 f(x)=x 的代入。"""

    RIGHT_EDGE = 0.95

    def build_left(self) -> VGroup:
        header = cn("帕塞瓦尔等式", 0.55)
        general = MathTex(
            r"f(x)\sim\frac{a_0}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n\cos(nx)+b_n\sin(nx)\right)"
        ).scale(0.6)
        condition = cn("条件：f 在 [−π, π] 上平方可积", 0.42)
        parseval = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)^2\,dx"
            r"=\frac{a_0^2}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n^2+b_n^2\right)"
        ).scale(0.6)
        note = cn("函数平方的积分 = 系数平方之和", 0.45)
        return VGroup(header, general, condition, parseval, note).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4
        )

    def build_right(self) -> tuple:
        series = MathTex(
            r"f(x)=x=",
            r"2\sum_{n=1}^{\infty}",
            r"\frac{(-1)^{n+1}}{n}",
            r"\sin(nx)",
        ).scale(0.6)
        sub = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx"
            r"=\sum_{n=1}^{\infty}\left(\frac{2(-1)^{n+1}}{n}\right)^2"
        ).scale(0.6)
        result = MathTex(
            r"S=\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}"
        ).scale(0.72)
        return series, sub, result

    def construct(self):
        title = heading("傅里叶级数与帕塞瓦尔等式", "Fourier Series and Parseval's Identity")
        left = self.build_left()
        header_l, general, condition, parseval, note = left
        series, sub, result = self.build_right()

        left.to_edge(LEFT, buff=0.5)
        left.align_to(UP * 2.3, UP)
        for item, ref in ((series, general), (sub, parseval), (result, note)):
            item.align_to(RIGHT * self.RIGHT_EDGE, LEFT)
            item.set_y(ref.get_y())
        divider = Line(
            UP * 2.5,
            UP * (min(left.get_bottom()[1], result.get_bottom()[1]) - 0.15),
            stroke_width=1.2,
            stroke_opacity=0.22,
        )
        divider.set_x((left.get_right()[0] + self.RIGHT_EDGE) / 2)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.9)
        self.wait(0.6)
        self.play(Create(divider), FadeIn(header_l), run_time=0.9)

        # 左栏：等式说的是什么
        self.wait(2.9)
        self.play(Write(general), run_time=1.4)
        self.wait(2.7)
        self.play(FadeIn(condition), run_time=0.9)
        self.wait(0.8)
        self.play(Write(parseval), run_time=1.6)
        self.play(FadeIn(note), run_time=0.8)

        # 右栏：同一行上把 f(x)=x 代进去
        self.wait(1.0)
        self.play(Write(series), run_time=1.5)
        self.wait(0.9)
        self.play(Write(sub), run_time=1.5)

        self.play(Write(result), run_time=1.4)
        self.play(Indicate(result, scale_factor=1.15), run_time=0.8)
        self.wait(0.6)
