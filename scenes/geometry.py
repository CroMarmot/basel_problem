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
    VGroup,
    Write,
    angle_of_vector,
)

from .common import ACCENT, EXTRA, cn, screen_title


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


class BaselGeometryLight(Scene):
    """屏幕 1：平方反比与亮度。"""

    def construct(self):
        title = screen_title("Wästlund 的几何证明", "平方反比看成接受光照")

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
        title = screen_title("Wästlund 的几何证明", "反勾股定理")

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
        title = screen_title("Wästlund 的几何证明", "一盏灯换成两盏等效灯")

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
        title = screen_title("Wästlund 的几何证明", "半径翻倍：N 等分换成 2N 等分")

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
    """屏幕 5：周长与灯数同步翻倍，圆在 P 附近趋于直线。"""

    def construct(self):
        title = screen_title("Wästlund 的几何证明", "极限：圆变成直线")

        P = LEFT * 4.4 + DOWN * 3.2
        r0 = 0.3
        circles = VGroup()
        lamp_groups = VGroup()
        lamp_points: list = []
        centers: list = []
        for k in range(4):
            radius = r0 * 2**k
            center = P + UP * radius
            centers.append(center)
            circles.add(
                Circle(radius=radius, color=WHITE, stroke_width=2.6).move_to(center)
            )
            points = []
            for s in range(1, 2 ** (k + 1), 2):
                theta = -np.pi / 2 + np.pi * s / 2**k
                points.append(
                    center + radius * np.array([np.cos(theta), np.sin(theta), 0.0])
                )
            lamp_points.append(points)
            lamp_groups.add(VGroup(*[star_at(pt, radius=0.062) for pt in points]))

        chords = VGroup()
        for k in range(3):
            group = VGroup()
            for point in lamp_points[k]:
                direction = np.array([-(point - P)[1], (point - P)[0], 0.0])
                a, b = chord_through(point, direction, centers[k + 1], r0 * 2 ** (k + 1))
                group.add(
                    Line(a, b, color=WHITE, stroke_width=1.6, stroke_opacity=0.55)
                )
            chords.add(group)

        guide = DashedLine(P, P + UP * (16 * r0), stroke_width=1.4, stroke_opacity=0.45)
        dot_P = Dot(P, radius=0.05, color=WHITE)
        label_P = MathTex("P").scale(0.5).next_to(P, DOWN, buff=0.18)

        note_1 = cn("初始：周长 2，灯在 P 的正对面", 0.44)
        f_bright = MathTex(r"\frac{1}{d^2}=\frac{1}{(2/\pi)^2}=\frac{\pi^2}{4}").scale(0.62)
        bright_row = VGroup(cn("总亮度：", 0.5), f_bright).arrange(RIGHT, buff=0.25)
        column = VGroup(note_1, bright_row).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        column.move_to(RIGHT * 3.3 + UP * 1.6)

        f_limit = MathTex(
            r"2\left(1+\frac{1}{9}+\frac{1}{25}+\cdots\right)=\frac{\pi^2}{4}"
        ).scale(0.8)
        f_limit.move_to(RIGHT * 3.3 + DOWN * 1.6)

        line_center = RIGHT * 3.3 + DOWN * 0.1
        unit = 0.42
        limit_line = Line(
            line_center + LEFT * 3.5,
            line_center + RIGHT * 3.5,
            color=WHITE,
            stroke_width=2,
        )
        dot_origin = Dot(line_center, radius=0.05, color=WHITE)
        label_origin = MathTex("P").scale(0.5).next_to(dot_origin, UP, buff=0.16)
        offsets = [-7, -5, -3, -1, 1, 3, 5, 7]
        line_lamps = VGroup(
            *[star_at(line_center + RIGHT * unit * v, radius=0.06) for v in offsets]
        )
        line_labels = VGroup(
            *[
                MathTex(str(v)).scale(0.42).next_to(
                    line_center + RIGHT * unit * v, DOWN, buff=0.18
                )
                for v in offsets
            ]
        )

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(
            Create(guide),
            Create(circles[0]),
            FadeIn(dot_P),
            FadeIn(label_P),
            FadeIn(lamp_groups[0]),
            run_time=1.4,
        )
        self.play(FadeIn(note_1, shift=UP), run_time=0.8)
        self.play(FadeIn(bright_row[0]), Write(f_bright), run_time=1.0)
        self.wait(4.0)

        self.play(Create(circles[1]), run_time=0.8)
        self.play(Create(chords[0]), run_time=0.7)
        self.play(FadeIn(lamp_groups[1]), run_time=0.6)
        self.wait(1.1)

        self.play(
            FadeOut(chords[0]),
            Create(circles[2]),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[Create(chord) for chord in chords[1]], lag_ratio=0.3),
            run_time=0.7,
        )
        self.play(FadeIn(lamp_groups[2]), run_time=0.6)

        self.play(
            FadeOut(chords[1]),
            Create(circles[3]),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[Create(chord) for chord in chords[2]], lag_ratio=0.25),
            run_time=0.9,
        )
        self.play(FadeIn(lamp_groups[3]), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(chords[2]),
            *[circle.animate.set_stroke(opacity=0.22) for circle in circles],
            *[lamps.animate.set_opacity(0.25) for lamps in lamp_groups],
            guide.animate.set_opacity(0.18),
            dot_P.animate.set_opacity(0.3),
            run_time=0.9,
        )
        self.play(Create(limit_line), FadeIn(dot_origin), FadeIn(label_origin), run_time=1.2)
        self.wait(2.2)
        self.play(
            LaggedStart(*[FadeIn(lamp) for lamp in line_lamps], lag_ratio=0.12),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[FadeIn(label) for label in line_labels], lag_ratio=0.1),
            run_time=1.2,
        )
        self.wait(0.5)
        self.play(Write(f_limit), run_time=1.6)
        self.wait(0.7)

        everything = VGroup(
            title, circles, lamp_groups, guide, dot_P, label_P, column,
            f_limit, limit_line, dot_origin, label_origin,
            line_lamps, line_labels,
        )
        self.play(FadeOut(everything), run_time=0.5)


TERM_COUNT = 5
GRID_COLUMNS = 4 * TERM_COUNT + 1


def _term(den: int) -> str:
    return "1" if den == 1 else r"\frac{1}{%d}" % den


def _grid_row(prefix: str, slots: dict, rhs: str = "") -> str:
    cells = {0: prefix, GRID_COLUMNS + 1: rhs}
    cells.update(slots)
    return "&".join(cells.get(index, "") for index in range(GRID_COLUMNS + 2))


def _odd_row() -> str:
    slots = {}
    for k in range(1, TERM_COUNT + 1):
        slots[4 * k - 3] = _term((2 * k - 1) ** 2)
        if k > 1:
            slots[4 * k - 4] = "+"
    slots[GRID_COLUMNS - 1] = "+"
    slots[GRID_COLUMNS] = r"\cdots"
    return _grid_row("", slots, r"=\frac{\pi^{2}}{8}")


def _whole_row() -> str:
    slots = {}
    for k in range(1, 2 * TERM_COUNT + 1):
        slots[2 * k - 1] = _term(k**2)
        if k < 2 * TERM_COUNT:
            slots[2 * k] = "+"
    slots[GRID_COLUMNS - 1] = "+"
    slots[GRID_COLUMNS] = r"\cdots"
    return _grid_row("S=", slots)


def _even_row() -> str:
    slots = {}
    for k in range(1, TERM_COUNT + 1):
        slots[4 * k - 1] = _term((2 * k) ** 2)
        if k > 1:
            slots[4 * k - 2] = "+"
    slots[GRID_COLUMNS - 1] = "+"
    slots[GRID_COLUMNS] = r"\cdots"
    return _grid_row(r"\frac{1}{4}S=", slots)


def _ruler_row() -> str:
    return _grid_row("", {index: r"\scriptstyle\cdot" for index in range(1, GRID_COLUMNS + 1)})


ODD_EVEN_GRID = (
    r"\begin{array}{r*{%d}{c}r}" % GRID_COLUMNS
    + _odd_row()
    + r"\\[12pt]"
    + _whole_row()
    + r"\\[46pt]"
    + _even_row()
    + r"\\[10pt]"
    + _ruler_row()
    + r"\end{array}"
)


class BaselGeometryResult(Scene):
    """屏幕 6：奇数项与偶数项合并回 S。"""

    def split_rows(self, grid: MathTex, count: int) -> list:
        leaves = [leaf for leaf in grid.get_family() if not leaf.submobjects]
        ys = sorted({round(leaf.get_center()[1], 3) for leaf in leaves})
        gaps = sorted(
            range(len(ys) - 1), key=lambda i: ys[i + 1] - ys[i], reverse=True
        )[: count - 1]
        cuts = sorted((ys[i] + ys[i + 1]) / 2 for i in gaps)
        rows = [VGroup() for _ in range(count)]
        for leaf in leaves:
            index = sum(cut < leaf.get_center()[1] for cut in cuts)
            rows[index].add(leaf)
        return sorted(rows, key=lambda row: -row.get_center()[1])

    def build_arrows(self, ruler: VGroup, row_all: VGroup, row_even: VGroup):
        columns = sorted(leaf.get_center()[0] for leaf in ruler)
        arrows = VGroup()
        labels = VGroup()
        top = row_all.get_bottom()[1]
        bot = row_even.get_top()[1]
        for k in range(1, TERM_COUNT + 1):
            # S 行里 1/k^2 占第 2k-1 列，偶数行里它对应的 1/(2k)^2 占第 4k-1 列。
            source = columns[2 * k - 2]
            target = columns[4 * k - 2]
            labels.add(
                MathTex(r"\times\frac{1}{4}")
                .scale(0.28)
                .move_to([source, top - 0.26, 0.0])
            )
            arrows.add(
                Arrow(
                    np.array([source, top - 0.52, 0.0]),
                    np.array([target, bot + 0.06, 0.0]),
                    buff=0.0,
                    stroke_width=4,
                    tip_length=0.13,
                    max_stroke_width_to_length_ratio=12,
                )
            )
        return arrows, labels

    def construct(self):
        title = screen_title("Wästlund 的几何证明", "回到巴塞尔问题")

        grid = MathTex(ODD_EVEN_GRID).scale(0.55)
        row_odd, row_all, row_even, ruler = self.split_rows(grid, 4)
        # 标尺行只用来取列位置，不入画，所以按可见的三行来定位。
        grid.shift(UP * 1.05 - VGroup(row_odd, row_all, row_even).get_center())
        arrows, labels = self.build_arrows(ruler, row_all, row_even)

        f_final = MathTex(
            r"S=\frac{\pi^2}{8}\cdot\frac{1}{1-\frac{1}{4}}=\frac{\pi^2}{6}"
        ).scale(0.85)
        f_final.move_to(DOWN * 1.6)

        credit = cn("Johan Wästlund · 2010 · 3Blue1Brown", 0.38)
        credit.to_edge(DOWN, buff=0.35)
        credit.set_opacity(0.7)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.play(FadeIn(row_odd), run_time=0.9)
        self.wait(3.6)
        self.play(FadeIn(row_all), run_time=0.9)
        self.wait(3.8)
        self.play(FadeIn(row_even), run_time=0.9)
        self.wait(0.4)
        self.play(
            LaggedStart(
                *[
                    animation
                    for pair in zip(arrows, labels)
                    for animation in (FadeIn(pair[0]), FadeIn(pair[1]))
                ],
                lag_ratio=0.12,
            ),
            run_time=1.3,
        )
        self.wait(2.4)
        self.wait(1.6)
        self.play(Write(f_final), run_time=1.6)
        self.wait(1.6)
        self.play(FadeIn(credit), run_time=0.5)
        self.play(f_final.animate.set_color(ACCENT), run_time=0.9)
        self.wait(0.4)
