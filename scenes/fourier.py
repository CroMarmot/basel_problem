from manim import DOWN, UP, MathTex, Scene, Text, VGroup, Write

from .common import ACCENT, CN_FONT


class BaselFourier(Scene):
    def construct(self):
        title = Text("严格证明：傅里叶级数", font=CN_FONT).to_edge(UP)
        fourier = MathTex(
            r"x=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)",
            r"\quad (-\pi<x<\pi)",
        )
        parseval = MathTex(
            r"\frac{1}{\pi}\int_{-\pi}^{\pi}x^2\,dx",
            "=",
            r"2\sum_{n=1}^{\infty}\frac{1}{n^2}",
        )
        calculation = MathTex(
            r"\frac{2\pi^2}{3}=2S",
            r"\quad\Rightarrow\quad",
            r"S=\frac{\pi^2}{6}",
        )
        calculation[-1].set_color(ACCENT)
        content = VGroup(fourier, parseval, calculation).arrange(DOWN, buff=0.55).scale(0.85)
        content.next_to(title, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(Write(fourier), run_time=1.5)
        self.wait(0.5)
        self.play(Write(parseval))
        self.wait(0.5)
        self.play(Write(calculation), run_time=1.5)
        self.wait(3)
