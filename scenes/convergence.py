from manim import DOWN, UP, MathTex, Scene, Text, VGroup, Write

from .common import ACCENT, CN_FONT


class BaselConvergence(Scene):
    def construct(self):
        title = Text("先证明它收敛", font=CN_FONT).to_edge(UP)
        line1 = MathTex(
            r"\frac{1}{n^2} < \frac{1}{n(n-1)} = \frac{1}{n-1}-\frac{1}{n}",
            r"\quad (n\ge 2)",
        )
        line2 = MathTex(
            r"\sum_{n=2}^{N}\frac{1}{n^2}",
            "<",
            r"\sum_{n=2}^{N}\left(\frac{1}{n-1}-\frac{1}{n}\right)",
            "=",
            r"1-\frac{1}{N}<1",
        )
        line3 = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{n^2}<2", color=ACCENT)
        content = VGroup(line1, line2, line3).arrange(DOWN, buff=0.55).scale(0.85)
        content.next_to(title, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)
        self.play(Write(line3))
        self.wait(3)
