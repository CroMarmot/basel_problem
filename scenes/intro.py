from manim import DOWN, ORIGIN, UP, FadeIn, MathTex, Scene, VGroup, Write

from .common import ACCENT, body, screen_title


class BaselIntro(Scene):
    def construct(self):
        title = screen_title("巴塞尔问题", "Basel Problem")
        question = body("所有正整数平方的倒数之和是多少？")
        equation = MathTex(
            r"S=",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            "=",
            r"1+\frac{1}{2^2}+\frac{1}{3^2}+\frac{1}{4^2}+\cdots",
            "=",
            "?",
        ).scale(0.8)
        equation[-1].set_color(ACCENT)
        content = VGroup(question, equation).arrange(DOWN, buff=0.95)
        content.move_to(ORIGIN)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=1.5)
        self.play(FadeIn(question, shift=UP), run_time=1.5)
        self.play(Write(equation), run_time=2)
        self.wait(1)
        self.play(equation[-1].animate.scale(1.3), run_time=0.6)
        self.play(equation[-1].animate.scale(1 / 1.3), run_time=0.6)
        self.wait(4)
