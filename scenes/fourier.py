from manim import DOWN, LEFT, RIGHT, UP, Line, MathTex, Scene, Text, VGroup, Write

from .common import CN_FONT


class BaselFourier(Scene):
    def construct(self):
        title = Text("傅里叶级数与帕塞瓦尔等式", font=CN_FONT)
        title.move_to(UP * 3.55)
        subtitle = Text("Fourier Series · Parseval's Identity", font_size=22)
        subtitle.next_to(title, DOWN, buff=0.08)

        divider = Line(UP * 2.45, DOWN * 3.72, stroke_width=1.2, stroke_opacity=0.22)

        left_header = Text("帕塞瓦尔等式", font=CN_FONT).scale(0.7)
        left_header.move_to(LEFT * 3.55 + UP * 2.0)
        right_header = Text("具体使用", font=CN_FONT).scale(0.7)
        right_header.move_to(RIGHT * 3.55 + UP * 2.0)

        left_condition = VGroup(
            Text("条件：f 平方可积", font=CN_FONT),
            Text("区间：[−π,π]", font=CN_FONT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).scale(0.55)
        left_fourier = MathTex(
            r"f(x)\sim\frac{a_0}{2}"
            r"+\sum_{n=1}^{\infty}\left(a_n\cos(nx)+b_n\sin(nx)\right)"
        ).scale(0.58)
        left_parseval = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)^2\,dx"
            r"=\frac{a_0^2}{2}+\sum_{n=1}^{\infty}\left(a_n^2+b_n^2\right)"
        ).scale(0.58)
        row_1 = UP * 1.25
        row_2 = UP * 0.20
        row_3 = DOWN * 0.90
        row_4 = DOWN * 2.00
        left_condition.move_to(LEFT * 3.55 + row_1)
        left_fourier.move_to(LEFT * 3.55 + row_2)
        left_parseval.move_to(LEFT * 3.55 + row_3)

        right_function = MathTex(r"f(x)=x,\quad -\pi<x<\pi").scale(0.66)
        right_series = MathTex(
            r"f(x)=x=",
            r"2\sum_{n=1}^{\infty}",
            r"\frac{(-1)^{n+1}}{n}",
            r"\sin(nx)",
        ).scale(0.64)
        right_integral = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx"
        ).scale(0.64)
        right_equals = MathTex("=").scale(0.64)
        right_sum = MathTex(
            r"\sum_{n=1}^{\infty}\left(\frac{2}{n}\right)^2"
        ).scale(0.64)
        right_parseval = VGroup(
            right_integral, right_equals, right_sum
        ).arrange(RIGHT, buff=0.09)
        right_result = MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            "=",
            r"\frac{\pi^2}{6}",
        ).scale(0.68)
        right_function.move_to(RIGHT * 3.55 + row_1)
        right_series.move_to(RIGHT * 3.55 + row_2)
        right_parseval.move_to(RIGHT * 3.55 + row_3)
        right_result.move_to(RIGHT * 3.55 + row_4)

        self.play(Write(title), Write(subtitle), run_time=1.2)
        self.play(Write(divider), Write(left_header), Write(right_header), run_time=0.6)
        self.play(Write(left_condition), Write(left_fourier), run_time=1.0)
        self.play(Write(left_parseval), run_time=1.0)
        self.play(Write(right_function), Write(right_series), run_time=1.0)
        self.play(Write(right_parseval), run_time=1.0)
        self.play(Write(right_result), run_time=1.0)
        self.wait(2.5)
