from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
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


class BaselFourierSeries(Scene):
    def construct(self):
        title = heading("傅里叶级数", "Fourier Series")

        general = MathTex(
            r"f(x)\sim\frac{a_0}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n\cos(nx)+b_n\sin(nx)\right)"
        ).scale(0.72)
        general.move_to(UP * 1.8)

        divider = Line(LEFT * 5.4, RIGHT * 5.4, stroke_width=1.2, stroke_opacity=0.22)
        divider.move_to(UP * 0.95)

        function = MathTex(r"f(x)=x,\quad -\pi<x<\pi").scale(0.82)
        function.move_to(UP * 0.25)

        series = MathTex(
            r"f(x)=x=",
            r"2\sum_{n=1}^{\infty}",
            r"\frac{(-1)^{n+1}}{n}",
            r"\sin(nx)",
        ).scale(0.88)
        series.move_to(DOWN * 1.05)

        note = cn("x 是奇函数，只剩正弦项", 0.5)
        note.move_to(DOWN * 2.2)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(Write(general), run_time=0.8)
        self.play(Create(divider), Write(function), run_time=0.8)
        self.play(Write(series), run_time=0.9)
        self.play(FadeIn(note, shift=UP), run_time=0.6)
        self.wait(2.5)


class BaselFourierParseval(Scene):
    def construct(self):
        title = heading("帕塞瓦尔等式", "Parseval's Identity")

        condition = cn("条件：f 在 [−π,π] 上平方可积", 0.55)
        condition.move_to(UP * 1.8)

        fourier = MathTex(
            r"f(x)\sim\frac{a_0}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n\cos(nx)+b_n\sin(nx)\right)"
        ).scale(0.62)
        fourier.move_to(UP * 0.75)

        parseval = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)^2\,dx"
            r"=\frac{a_0^2}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n^2+b_n^2\right)"
        ).scale(0.85)
        parseval.move_to(DOWN * 0.65)

        note = cn("函数平方的积分 = 系数平方和", 0.5)
        note.move_to(DOWN * 2.1)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(FadeIn(condition, shift=UP), run_time=0.7)
        self.play(Write(fourier), run_time=0.8)
        self.play(Write(parseval), run_time=1.0)
        self.play(FadeIn(note, shift=UP), run_time=0.6)
        self.wait(2.5)


class BaselFourierResult(Scene):
    def construct(self):
        title = heading("代入帕塞瓦尔等式", "From Parseval to Basel")

        series = MathTex(
            r"f(x)=x=",
            r"2\sum_{n=1}^{\infty}",
            r"\frac{(-1)^{n+1}}{n}",
            r"\sin(nx)",
        ).scale(0.68)
        series.move_to(UP * 1.85)

        parseval = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx"
            r"=\sum_{n=1}^{\infty}\left(\frac{2}{n}\right)^2"
        ).scale(0.82)
        parseval.move_to(UP * 0.45)

        simplify = cn("化简", 0.45)
        simplify.move_to(DOWN * 0.45)

        result = MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            "=",
            r"\frac{\pi^2}{6}",
        ).scale(1.0)
        result.move_to(DOWN * 1.55)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(Write(series), run_time=0.8)
        self.play(Write(parseval), run_time=0.9)
        self.play(FadeIn(simplify, shift=DOWN), run_time=0.5)
        self.play(Write(result), run_time=0.9)
        self.wait(2.5)
