from manim import DOWN, FadeIn, MathTex, Scene, Write

from .common import ACCENT, screen_title


class BaselEuler(Scene):
    def construct(self):
        title = screen_title("欧拉的无穷乘积", "类比多项式的因式分解")
        derivation = MathTex(
            r"\begin{aligned}"
            r"1-\left(\sum_{n=1}^{\infty}\frac{1}{n^2\pi^2}\right)x^2+\cdots"
            r"&=\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)\\"
            r"&=\prod_{n=1}^{\infty}\left(1-\frac{x}{n\pi}\right)\left(1+\frac{x}{n\pi}\right)\\"
            r"&=\frac{\sin x}{x}\\"
            r"&=1-\frac{x^2}{6}+\frac{x^4}{120}-\cdots"
            r"\end{aligned}",
            substrings_to_isolate=[
                r"-\left(\sum_{n=1}^{\infty}\frac{1}{n^2\pi^2}\right)x^2",
                r"-\frac{x^2}{6}",
            ],
        ).scale(0.6)
        derivation.next_to(title, DOWN, buff=0.3)
        left_coef = derivation.get_part_by_tex(
            r"-\left(\sum_{n=1}^{\infty}\frac{1}{n^2\pi^2}\right)x^2"
        )
        right_coef = derivation.get_part_by_tex(r"-\frac{x^2}{6}")
        result = MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}",
            color=ACCENT,
        )
        result.next_to(derivation, DOWN, buff=0.35)

        self.play(Write(title[0]), FadeIn(title[1]))
        self.play(Write(derivation), run_time=2.5)
        self.wait(0.5)
        self.play(
            left_coef.animate.set_color(ACCENT),
            right_coef.animate.set_color(ACCENT),
            run_time=0.8,
        )
        self.wait(1)
        self.play(Write(result), run_time=1.5)
        self.wait(10.0)
