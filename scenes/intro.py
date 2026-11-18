from manim import DOWN, ORIGIN, RIGHT, UP, FadeIn, MathTex, Scene, Text, VGroup, Write

from .common import ACCENT, CN_FONT


class BaselIntro(Scene):
    def construct(self):
        title_cn = Text("巴塞尔问题", font=CN_FONT, font_size=64)
        title_en = Text("Basel Problem", font_size=34)
        title = VGroup(title_cn, title_en).arrange(
            RIGHT, buff=0.45, aligned_edge=DOWN
        )
        question = Text("所有正整数平方的倒数之和是多少？", font=CN_FONT, font_size=40)
        equation = MathTex(
            r"S=",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            "=",
            r"1+\frac{1}{4}+\frac{1}{9}+\frac{1}{16}+\cdots",
            "=",
            "?",
        ).scale(0.8)
        equation[-1].set_color(ACCENT)
        content = VGroup(title, question, equation).arrange(DOWN, buff=0.85)
        content.move_to(ORIGIN)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(question, shift=UP), run_time=1.5)
        self.play(Write(equation), run_time=2)
        self.wait(1)
        self.play(equation[-1].animate.scale(1.3), run_time=0.6)
        self.play(equation[-1].animate.scale(1 / 1.3), run_time=0.6)
        self.wait(4)
