from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    MathTex,
    Polygon,
    Scene,
    Text,
    VGroup,
    Write,
)

from .common import ACCENT, CN_FONT


class BaselGeometry(Scene):
    def construct(self):
        title = Text("几何证明：Wästlund", font=CN_FONT).to_edge(UP)
        subtitle = Text("用欧几里得几何求平方倒数和", font=CN_FONT, font_size=30)
        subtitle.next_to(title, DOWN, buff=0.25)

        A = LEFT * 2.8 + DOWN * 1.4
        B = RIGHT * 2.8 + DOWN * 1.4
        C = UP * 1.4
        D = DOWN * 1.4

        circle = Circle(radius=2.8, color=WHITE, stroke_opacity=0.2).move_to(D)
        triangle = Polygon(A, B, C, color=WHITE, stroke_width=4)
        altitude = DashedLine(C, D, color=ACCENT, stroke_width=3)
        labels = VGroup(
            MathTex("a").move_to((A + C) / 2 + LEFT * 0.3),
            MathTex("b").move_to((B + C) / 2 + RIGHT * 0.3),
            MathTex("h").next_to(altitude, RIGHT, buff=0.15),
        )
        diagram = VGroup(circle, triangle, altitude, labels)
        diagram.scale(0.8).shift(LEFT * 3.2 + UP * 0.4)

        formula = MathTex(
            r"\frac{1}{h^2}",
            "=",
            r"\frac{1}{a^2}",
            "+",
            r"\frac{1}{b^2}",
        ).scale(1.15)
        formula.move_to(RIGHT * 3.2 + UP * 0.9)
        caption = Text("反勾股定理", font=CN_FONT, font_size=30, color=ACCENT)
        caption.next_to(formula, DOWN, buff=0.35)

        odd = MathTex(
            r"1+\frac{1}{9}+\frac{1}{25}+\cdots",
            "=",
            r"\frac{\pi^2}{8}",
        ).scale(1.1)
        odd.move_to(UP * 1.5)
        even_note = Text("偶数项之和是总和的四分之一", font=CN_FONT, font_size=34)
        even_note.next_to(odd, DOWN, buff=0.55)
        relation = MathTex(
            r"S=\frac{4}{3}\cdot\frac{\pi^2}{8}=\frac{\pi^2}{6}"
        ).scale(1.15)
        relation.next_to(even_note, DOWN, buff=0.45)

        credit = Text("Johan Wästlund · 2010", font=CN_FONT, font_size=24)
        credit.to_edge(DOWN)
        credit.set_opacity(0.7)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(Create(circle), Create(triangle), Create(altitude))
        self.wait(3)
        self.play(Write(labels), Write(formula), FadeIn(caption))
        self.wait(4)

        self.play(
            FadeOut(diagram),
            FadeOut(formula),
            FadeOut(caption),
            FadeOut(subtitle),
        )
        self.wait(0.5)
        self.play(Write(odd))
        self.wait(2)
        self.play(FadeIn(even_note, shift=UP))
        self.wait(2)
        self.play(Write(relation))
        self.wait(2)
        self.play(FadeIn(credit))
        self.wait(0.5)
        self.play(relation.animate.set_color(ACCENT), run_time=1.5)
        self.wait(1)
        self.play(relation.animate.set_color(WHITE), run_time=1.5)
        self.wait(4)
