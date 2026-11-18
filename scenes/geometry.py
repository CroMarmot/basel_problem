import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    WHITE,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Scene,
    Text,
    VGroup,
    Write,
    angle_of_vector,
)

from .common import ACCENT, CN_FONT


def cn(text: str, scale: float = 0.55, color=WHITE) -> Text:
    return Text(text, font=CN_FONT, color=color).scale(scale)


def heading(title_text: str, subtitle_text: str) -> VGroup:
    title = cn(title_text, 0.8)
    title.to_edge(UP, buff=0.4)
    subtitle = Text(subtitle_text, font=CN_FONT, font_size=22).scale(0.42)
    subtitle.next_to(title, DOWN, buff=0.1)
    return VGroup(title, subtitle)


def star_at(point, color=ACCENT, radius: float = 0.07) -> VGroup:
    glow = Circle(
        radius=radius * 2.6,
        color=color,
        stroke_width=0,
        fill_opacity=0.16,
    ).move_to(point)
    dot = Dot(point, radius=radius, color=color)
    return VGroup(glow, dot)


def unit(vector) -> np.ndarray:
    return vector / np.linalg.norm(vector)


def right_angle_mark(vertex, arm_a, arm_b, size: float = 0.2) -> VGroup:
    u = unit(arm_a - vertex)
    v = unit(arm_b - vertex)
    p1 = vertex + u * size
    p2 = p1 + v * size
    p3 = vertex + v * size
    return VGroup(
        Line(p1, p2, color=WHITE, stroke_width=2),
        Line(p2, p3, color=WHITE, stroke_width=2),
    )


def screen_corners(center, width: float, height: float, slant: float) -> list:
    w = width / 2
    h = height / 2
    return [
        center + LEFT * w + DOWN * h,
        center + RIGHT * w + DOWN * h,
        center + RIGHT * w + UP * h + RIGHT * slant,
        center + LEFT * w + UP * h + RIGHT * slant,
    ]


def quad(points, stroke_width: float = 2) -> Polygon:
    return Polygon(
        *points,
        color=WHITE,
        stroke_width=stroke_width,
        fill_opacity=0.05,
    )


def project(points, source, ratio: float) -> list:
    """以光源为位似中心截取锥面，保证角点严格落在光线上。"""
    return [source + (point - source) * ratio for point in points]


def chord_through(point, direction, center, radius: float) -> tuple:
    """直线 point + t*direction 与圆 (center, radius) 的两个交点。"""
    d = unit(direction)
    f = point - center
    b = float(np.dot(d, f))
    c = float(np.dot(f, f)) - radius**2
    half = np.sqrt(max(b * b - c, 0.0))
    return point + d * (-b + half), point + d * (-b - half)


def mini_circle(baseline, radius: float, angles: list[float], label: str) -> VGroup:
    center = baseline + UP * radius
    ground = Line(
        baseline + LEFT * (radius + 0.2),
        baseline + RIGHT * (radius + 0.2),
        color=WHITE,
        stroke_width=2,
    )
    circle = Circle(radius=radius, color=WHITE, stroke_width=2).move_to(center)
    stars = VGroup(
        *[
            star_at(
                center
                + RIGHT * radius * np.sin(angle)
                + DOWN * radius * np.cos(angle),
                radius=0.045,
            )
            for angle in angles
        ]
    )
    caption = cn(label, 0.36).next_to(baseline, DOWN, buff=0.08)
    return VGroup(ground, circle, stars, caption)


class BaselGeometryLight(Scene):
    """屏幕 1：平方反比与亮度。"""

    def construct(self):
        title = heading("几何证明：Wästlund", "用欧几里得几何求平方倒数和")

        source_pt = LEFT * 3.5 + UP * 2.4
        far_points = screen_corners(LEFT * 3.5 + DOWN * 1.9, 2.6, 2.0, 0.26)
        near_points = project(far_points, source_pt, 0.5)

        source = star_at(source_pt, radius=0.11)
        near_screen = quad(near_points)
        far_screen = quad(far_points)
        light_rays = VGroup(
            *[
                DashedLine(source_pt, point, color=WHITE, stroke_width=1.2, stroke_opacity=0.35)
                for point in far_points
            ]
        )
        near_label = VGroup(
            cn("距离 d", 0.38),
            cn("面积 A", 0.38),
            cn("亮度 B", 0.38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        near_label.next_to(near_screen, RIGHT, buff=0.25)
        far_label = VGroup(
            cn("距离 2d", 0.4),
            cn("面积 4A", 0.4),
            cn("亮度 B/4", 0.4, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        far_label.next_to(far_screen, RIGHT, buff=0.25)

        light_formula = MathTex(r"B\propto\frac{1}{r^2}").scale(0.95)
        light_formula.move_to(RIGHT * 2.7 + UP * 1.25)
        light_caption = cn("距离翻倍，亮度只剩四分之一", 0.5)
        light_caption.next_to(light_formula, DOWN, buff=0.5)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=1.0)
        self.play(FadeIn(source), Create(light_rays), run_time=1.0)
        self.play(Create(near_screen), FadeIn(near_label), run_time=0.8)
        self.wait(1.0)
        self.play(Create(far_screen), FadeIn(far_label), run_time=0.8)
        self.wait(1.0)
        self.play(Write(light_formula), FadeIn(light_caption), run_time=0.9)
        self.wait(3.3)

        everything = VGroup(
            title, source, light_rays, near_screen, far_screen,
            near_label, far_label, light_formula, light_caption,
        )
        self.play(FadeOut(everything), run_time=0.5)


class BaselGeometryPythagoras(Scene):
    """屏幕 2：反勾股定理。"""

    def construct(self):
        title = heading("反勾股定理", "Inverse Pythagorean Theorem")

        A = LEFT * 5.9 + DOWN * 1.7
        B = LEFT * 1.5 + DOWN * 1.7
        C = LEFT * 3.0 + UP * 0.43
        H = LEFT * 3.0 + DOWN * 1.7

        triangle = Polygon(A, B, C, color=WHITE, stroke_width=4)
        altitude = Line(C, H, color=ACCENT, stroke_width=3)
        triangle_marks = VGroup(
            right_angle_mark(C, A, B, 0.22),
            right_angle_mark(H, C, B, 0.17),
        )
        triangle_labels = VGroup(
            MathTex("a").scale(0.75).move_to((A + C) / 2 + LEFT * 0.25),
            MathTex("b").scale(0.75).move_to((B + C) / 2 + RIGHT * 0.25),
            MathTex("h").scale(0.75).move_to((C + H) / 2 + RIGHT * 0.18),
            MathTex("c").scale(0.75).move_to((A + B) / 2 + DOWN * 0.22),
            MathTex("C").scale(0.6).next_to(C, UP, buff=0.08),
            MathTex("A").scale(0.6).next_to(A, DOWN + LEFT, buff=0.06),
            MathTex("B").scale(0.6).next_to(B, DOWN + RIGHT, buff=0.06),
        )
        pythagoras_formula = MathTex(
            r"\frac{1}{h^2}", "=", r"\frac{1}{a^2}", "+", r"\frac{1}{b^2}"
        ).scale(1.0)
        pythagoras_formula.move_to(RIGHT * 3.8 + UP * 0.8)
        pythagoras_note = cn("面积法：ab = ch，再用 c² = a² + b²", 0.4)
        pythagoras_note.next_to(pythagoras_formula, DOWN, buff=0.45)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.9)
        self.play(Create(triangle), Create(altitude), FadeIn(triangle_marks), run_time=1.0)
        self.play(Write(triangle_labels), run_time=0.8)
        self.wait(1.0)
        self.play(Write(pythagoras_formula), FadeIn(pythagoras_note), run_time=0.9)
        self.wait(4.1)

        everything = VGroup(
            title, triangle, altitude, triangle_marks, triangle_labels,
            pythagoras_formula, pythagoras_note,
        )
        self.play(FadeOut(everything), run_time=0.5)


class BaselGeometryCircle(Scene):
    """屏幕 3：过 R 作 RP 的垂线，把一颗星换成两颗星。"""

    def construct(self):
        title = heading("圆上的替换", "One Star Becomes Two")

        P = LEFT * 3.3 + DOWN * 2.35
        r1, r2 = 1.2, 2.4
        O1 = P + UP * r1
        O2 = P + UP * r2

        phi = np.deg2rad(115)
        R = O1 + RIGHT * r1 * np.sin(phi) + DOWN * r1 * np.cos(phi)
        normal = np.array([-(R - P)[1], (R - P)[0], 0.0])
        S1, S2 = sorted(chord_through(R, normal, O2, r2), key=lambda p: -p[0])

        circle1 = Circle(radius=r1, color=WHITE, stroke_width=3).move_to(O1)
        circle2 = Circle(radius=r2, color=WHITE, stroke_width=3).move_to(O2)
        dot_O1 = Dot(O1, radius=0.05, color=WHITE)
        dot_O2 = Dot(O2, radius=0.05, color=WHITE)
        perpendicular = DashedLine(S2, S1, color=WHITE, stroke_width=2, dash_length=0.12)
        altitude_pr = Line(P, R, color=ACCENT, stroke_width=3)
        side_1 = Line(P, S1, color=WHITE, stroke_width=2)
        side_2 = Line(P, S2, color=WHITE, stroke_width=2)
        angle_R = right_angle_mark(R, P, S1, 0.18)
        angle_P = right_angle_mark(P, S1, S2, 0.22)
        star_R = star_at(R, radius=0.085)
        star_S1 = star_at(S1, radius=0.07)
        star_S2 = star_at(S2, radius=0.07)
        circle_labels = VGroup(
            MathTex("R").scale(0.7).next_to(R, UP, buff=0.12),
            MathTex("S_1").scale(0.7).next_to(S1, RIGHT, buff=0.1),
            MathTex("S_2").scale(0.7).next_to(S2, LEFT, buff=0.1),
            MathTex("P").scale(0.7).next_to(P, DOWN, buff=0.12),
        )

        cond_radius = VGroup(
            cn("大圆半径是小圆的两倍", 0.42),
            MathTex(r"r_2=2r_1").scale(0.5),
        ).arrange(RIGHT, buff=0.28)
        cond_perp = VGroup(
            cn("PR 垂直于 S1S2", 0.42),
            MathTex(r"PR\perp S_1S_2").scale(0.5),
        ).arrange(RIGHT, buff=0.28)
        star_formula = MathTex(
            r"\frac{1}{PR^2}",
            "=",
            r"\frac{1}{PS_1^2}",
            "+",
            r"\frac{1}{PS_2^2}",
        ).scale(0.8)
        star_conclusion = cn("小圆上一盏灯的亮度 = 大圆上两盏灯的等效亮度", 0.46, color=ACCENT)
        column = VGroup(cond_radius, cond_perp, star_formula, star_conclusion).arrange(
            DOWN, aligned_edge=LEFT, buff=0.34
        )
        column.move_to(RIGHT * 3.0 + UP * 0.15)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(Create(circle1), FadeIn(dot_O1), run_time=0.9)
        self.play(FadeIn(star_R), FadeIn(circle_labels[0]), run_time=0.6)
        self.play(Create(altitude_pr), FadeIn(circle_labels[3]), run_time=0.7)
        self.wait(4.1)
        self.play(Create(circle2), FadeIn(dot_O2), run_time=1.0)
        self.play(FadeIn(cond_radius, shift=UP), run_time=0.8)
        self.wait(3.8)
        self.play(Create(perpendicular), FadeIn(angle_R), run_time=1.0)
        self.play(FadeIn(star_S1), FadeIn(star_S2), FadeIn(circle_labels[1:3]), run_time=0.9)
        self.play(Create(side_1), Create(side_2), FadeIn(angle_P), run_time=1.0)
        self.play(FadeIn(cond_perp, shift=UP), run_time=0.7)
        self.wait(4.7)
        self.play(Write(star_formula), run_time=1.4)
        self.wait(2.7)
        self.play(FadeIn(star_conclusion, shift=UP), run_time=0.9)
        self.wait(6.3)

        everything = VGroup(
            title, circle1, circle2, dot_O1, dot_O2,
            perpendicular, altitude_pr, side_1, side_2, angle_R, angle_P,
            star_R, star_S1, star_S2, circle_labels, column,
        )
        self.play(FadeOut(everything), run_time=0.5)


class BaselGeometryDoubling(Scene):
    """屏幕 4：小圆的 N 等分点逐盏换成大圆上对应的 2N 等分点。"""

    def construct(self):
        title = heading("翻倍与对应", "N Points Become 2N")

        P = LEFT * 3.55 + DOWN * 2.3
        r1, r2 = 1.1, 2.2
        O1 = P + UP * r1
        O2 = P + UP * r2

        lamp_points = [
            O1 + RIGHT * r1 * np.sin(a) + UP * r1 * np.cos(a)
            for a in np.deg2rad([40, 130, 220, 310])
        ]
        small_lamps = VGroup(*[star_at(pt, radius=0.075) for pt in lamp_points])

        diameters = VGroup()
        big_points = []
        for point in lamp_points:
            direction = unit(point - O2)
            forward = O2 + direction * r2
            backward = O2 - direction * r2
            diameters.add(
                Line(
                    backward,
                    forward,
                    color=WHITE,
                    stroke_width=1.6,
                    stroke_opacity=0.55,
                )
            )
            big_points += [forward, backward]
        big_lamps = VGroup(*[star_at(pt, radius=0.055) for pt in big_points])

        circle1 = Circle(radius=r1, color=WHITE, stroke_width=3).move_to(O1)
        circle2 = Circle(radius=r2, color=WHITE, stroke_width=3).move_to(O2)
        dot_O1 = Dot(O1, radius=0.05, color=WHITE)
        dot_O2 = Dot(O2, radius=0.05, color=WHITE)
        label_P = MathTex("P").scale(0.55).next_to(P, DOWN, buff=0.26)

        order = sorted(angle_of_vector(pt - O2) for pt in big_points)
        gap = 2 * np.pi / len(big_points)
        mark = 0.24
        angle_arcs = VGroup(
            *[
                Arc(
                    radius=0.34,
                    start_angle=order[i] + (gap - mark) / 2,
                    angle=mark,
                    arc_center=O2,
                    color=WHITE,
                    stroke_width=2.5,
                )
                for i in range(len(big_points))
            ]
        )

        label_O2 = MathTex("O_2").scale(0.55).next_to(O2, UL, buff=0.32)

        angle_lines = VGroup(
            VGroup(cn("观察汇聚于", 0.44), MathTex("O_2").scale(0.44), cn("的角", 0.44)).arrange(
                RIGHT, aligned_edge=DOWN, buff=0.1
            ),
            cn("对于小圆来说，圆周角两两相等", 0.44),
            cn("对于大圆来说，圆心角两两相等", 0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        conclusion = VGroup(
            cn("小圆的 N 等分点 = 大圆上", 0.46),
            cn("「对应的」", 0.46, color=ACCENT),
            cn("2N 等分点", 0.46),
        ).arrange(RIGHT, aligned_edge=DOWN, buff=0.09)
        column = VGroup(angle_lines, conclusion).arrange(
            DOWN, aligned_edge=LEFT, buff=0.62
        )
        column.move_to(RIGHT * 3.0 + UP * 0.55)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(Create(circle1), FadeIn(dot_O1), FadeIn(label_P), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(lamp) for lamp in small_lamps], lag_ratio=0.3),
            run_time=1.1,
        )
        self.wait(0.15)
        self.play(Create(circle2), FadeIn(dot_O2), FadeIn(label_O2), run_time=0.9)
        self.play(
            LaggedStart(*[Create(line) for line in diameters], lag_ratio=0.25),
            run_time=1.6,
        )
        self.play(
            LaggedStart(*[FadeIn(lamp) for lamp in big_lamps], lag_ratio=0.12),
            run_time=1.1,
        )
        self.wait(0.4)
        self.play(Create(angle_arcs), run_time=1.1)
        self.play(FadeIn(angle_lines[0], shift=UP), run_time=0.7)
        self.wait(1.0)
        self.play(FadeIn(angle_lines[1], shift=UP), run_time=0.7)
        self.wait(3.0)
        self.play(FadeIn(angle_lines[2], shift=UP), run_time=0.7)
        self.wait(3.3)
        self.play(FadeIn(conclusion, shift=UP), run_time=1.0)
        self.wait(6.1)

        everything = VGroup(
            title, circle1, circle2, dot_O1, dot_O2, label_P, label_O2,
            small_lamps, big_lamps, diameters, angle_arcs, column,
        )
        self.play(FadeOut(everything), run_time=0.5)


class BaselGeometryLimit(Scene):
    """屏幕 4：半径与星数同步翻倍，圆趋于直线。"""

    def construct(self):
        title = heading("翻倍与极限", "Doubling to a Line")

        baseline_1 = LEFT * 5.5 + DOWN * 2.45
        baseline_2 = LEFT * 3.55 + DOWN * 2.45
        baseline_3 = LEFT * 1.55 + DOWN * 2.45
        mini_1 = mini_circle(baseline_1, 0.48, [np.deg2rad(120)], "1 颗星")
        mini_2 = mini_circle(
            baseline_2, 0.58, [np.deg2rad(60), np.deg2rad(240)], "2 颗星"
        )
        mini_3 = mini_circle(
            baseline_3,
            0.68,
            [np.deg2rad(30), np.deg2rad(120), np.deg2rad(210), np.deg2rad(300)],
            "4 颗星",
        )
        mini_row = VGroup(mini_1, mini_2, mini_3)
        doubling_note = cn("半径 ×2，星数 ×2；切点亮度不变", 0.46)
        doubling_note.move_to(LEFT * 3.5 + UP * 1.35)

        limit_arrow = Arrow(
            LEFT * 0.55 + DOWN * 2.45,
            RIGHT * 0.25 + DOWN * 2.45,
            color=WHITE,
            stroke_width=2.5,
            buff=0,
        )
        limit_line = Line(
            RIGHT * 0.55 + DOWN * 2.45,
            RIGHT * 2.45 + DOWN * 2.45,
            color=WHITE,
            stroke_width=2,
        )
        limit_ticks = VGroup(
            *[
                Line(
                    RIGHT * x + DOWN * 2.55,
                    RIGHT * x + DOWN * 2.35,
                    color=WHITE,
                    stroke_width=2,
                )
                for x in [0.9, 1.3, 1.7, 2.1]
            ]
        )
        limit_label = cn("极限：半整数点", 0.36)
        limit_label.next_to(limit_line, DOWN, buff=0.08)
        limit_group = VGroup(limit_arrow, limit_line, limit_ticks, limit_label)

        half_integer_sum = MathTex(
            r"\sum_{m=-\infty}^{\infty}\frac{1}{\left(m+\frac12\right)^2}",
            "=",
            r"\pi^2",
        ).scale(0.85)
        half_integer_sum.move_to(RIGHT * 3.9 + UP * 0.9)
        odd_sum = MathTex(
            r"1+\frac{1}{9}+\frac{1}{25}+\cdots",
            "=",
            r"\frac{\pi^2}{8}",
        ).scale(0.9)
        odd_sum.move_to(RIGHT * 3.9 + DOWN * 0.35)
        pair_note = cn("正负半整数配对", 0.44)
        pair_note.next_to(odd_sum, DOWN, buff=0.3)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(FadeIn(mini_1), run_time=0.5)
        self.wait(1.4)
        self.play(FadeIn(mini_2), run_time=0.5)
        self.wait(1.4)
        self.play(FadeIn(mini_3), FadeIn(doubling_note), run_time=0.7)
        self.wait(3.3)
        self.play(Create(limit_group), run_time=0.7)
        self.play(Write(half_integer_sum), run_time=0.9)
        self.wait(2.8)
        self.play(Write(odd_sum), FadeIn(pair_note), run_time=0.9)
        self.wait(7.6)

        everything = VGroup(
            title, mini_row, doubling_note, limit_group, half_integer_sum, odd_sum, pair_note
        )
        self.play(FadeOut(everything), run_time=0.5)


class BaselGeometryResult(Scene):
    """屏幕 5：偶数项与奇数项合并回 S。"""

    def construct(self):
        title = heading("回到巴塞尔问题", "Back to Basel")

        line_1 = MathTex(r"S=1+\frac{1}{4}+\frac{1}{9}+\cdots").scale(0.85)
        line_2 = cn("偶数项 = S/4，奇数项 = 3S/4", 0.55)
        line_3 = MathTex(r"\frac{3S}{4}=\frac{\pi^2}{8}").scale(0.9)
        line_4 = MathTex(
            r"S=\frac{4}{3}\cdot\frac{\pi^2}{8}=\frac{\pi^2}{6}"
        ).scale(1.0)
        algebra = VGroup(line_1, line_2, line_3, line_4).arrange(DOWN, buff=0.32)
        algebra.move_to(DOWN * 0.25)

        credit = cn("Johan Wästlund · 2010 · 3Blue1Brown", 0.38)
        credit.to_edge(DOWN, buff=0.35)
        credit.set_opacity(0.7)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(Write(line_1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(line_2, shift=UP), run_time=0.6)
        self.wait(0.8)
        self.play(Write(line_3), run_time=0.7)
        self.play(Write(line_4), run_time=0.8)
        self.play(FadeIn(credit), run_time=0.5)
        self.play(line_4.animate.set_color(ACCENT), run_time=1.0)
        self.wait(3.0)
