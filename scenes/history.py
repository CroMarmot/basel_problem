from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    Indicate,
    MathTex,
    Scene,
    VGroup,
    Write,
)

from .common import ACCENT, body, screen_title


class BaselHistory(Scene):
    def construct(self):
        title = screen_title("从蒙戈利到欧拉", "Mengoli, Euler")
        euler_result = VGroup(
            body("1735 年，欧拉（Leonhard Euler）得到"),
            MathTex(r"\frac{\pi^2}{6}", color=ACCENT).scale(0.5),
        ).arrange(RIGHT, buff=0.12)
        items = VGroup(
            body("1644 年，蒙戈利（Pietro Mengoli）提出平方倒数和问题"),
            body("伯努利兄弟（Jakob & Johann Bernoulli）研究但未能求出精确值"),
            euler_result,
            body("欧拉因此声名大噪"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        items.next_to(title, DOWN, buff=0.6)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(items[0], shift=RIGHT), run_time=0.8)
        self.wait(2.7)
        self.play(FadeIn(items[1], shift=RIGHT), run_time=0.8)
        self.wait(1.9)
        self.play(FadeIn(items[2], shift=RIGHT), run_time=1.0)
        self.wait(4.2)
        self.play(Indicate(euler_result[1], scale_factor=1.4), run_time=1.0)
        self.wait(0.7)
        self.play(FadeIn(items[3], shift=RIGHT), run_time=0.9)
        self.wait(0.4)
