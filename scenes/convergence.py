from manim import DOWN, UP, MathTex, Scene, Text, Write

from .common import ACCENT, CN_FONT


class BaselConvergence(Scene):
    def construct(self):
        title = Text("先证明它收敛", font=CN_FONT).to_edge(UP)
        derivation = MathTex(
            r"\begin{aligned}"
            r"S&=\sum_{n=1}^{\infty}\frac{1}{n^2}"
            r"=1+\sum_{n=2}^{\infty}\frac{1}{n^2}\\"
            r"&<1+\sum_{n=2}^{\infty}\frac{1}{n(n-1)}"
            r"=1+\sum_{n=2}^{\infty}\left(\frac{1}{n-1}-\frac{1}{n}\right)\\"
            r"&=2."
            r"\end{aligned}",
            tex_to_color_map={"=2.": ACCENT},
        ).scale(0.85)
        derivation.next_to(title, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(Write(derivation), run_time=2.5)
        self.wait(3)
