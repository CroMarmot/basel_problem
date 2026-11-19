from manim import DOWN, LEFT, RIGHT, UP, FadeIn, LaggedStart, MathTex, Scene, Text, VGroup, Write

from .common import ACCENT, CN_FONT


class BaselHistory(Scene):
    def construct(self):
        title_cn = Text("从蒙戈利到欧拉", font=CN_FONT, font_size=44)
        title_en = Text("Basel Problem · Mengoli to Euler", font_size=28)
        title = VGroup(title_cn, title_en).arrange(DOWN, buff=0.15).to_edge(UP)
        euler_result = VGroup(
            Text("1735 年，欧拉（Leonhard Euler）得到", font=CN_FONT),
            MathTex(r"\frac{\pi^2}{6}", color=ACCENT).scale(0.9),
        ).arrange(RIGHT, buff=0.12)
        items = (
            VGroup(
                Text("1644 年，蒙戈利（Pietro Mengoli）提出平方倒数和问题", font=CN_FONT),
                Text(
                    "伯努利兄弟（Jakob & Johann Bernoulli）研究但未能求出精确值",
                    font=CN_FONT,
                ),
                euler_result,
                Text("欧拉因此声名大噪", font=CN_FONT),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            .scale(0.58)
        )
        items.next_to(title, DOWN, buff=0.55)

        self.play(Write(title))
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=RIGHT) for item in items],
                lag_ratio=0.25,
            )
        )
        self.wait(3)
