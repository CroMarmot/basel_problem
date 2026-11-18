from manim import DOWN, UP, MathTex, Scene, Text, VGroup, Write

from .common import ACCENT, CN_FONT


class BaselEuler(Scene):
    def construct(self):
        title = Text("欧拉的无穷乘积", font=CN_FONT).to_edge(UP)
        product = MathTex(
            r"\frac{\sin x}{x}=\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)"
        )
        expansion = MathTex(
            r"\frac{\sin x}{x}=1-\frac{x^2}{6}+\frac{x^4}{120}-\cdots"
        )
        compare = MathTex(
            r"-\frac{1}{6}=-\sum_{n=1}^{\infty}\frac{1}{n^2\pi^2}"
        )
        result = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}", color=ACCENT)
        content = VGroup(product, expansion, compare, result).arrange(DOWN, buff=0.45).scale(0.85)
        content.next_to(title, DOWN, buff=0.6)

        self.play(Write(title))
        self.play(Write(product), run_time=1.5)
        self.wait(0.5)
        self.play(Write(expansion))
        self.wait(0.5)
        self.play(Write(compare))
        self.wait(0.5)
        self.play(Write(result), run_time=1.5)
        self.wait(3)
