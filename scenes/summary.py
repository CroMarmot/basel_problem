import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    WHITE,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Scene,
    SurroundingRectangle,
    VGroup,
    Write,
)
from pathlib import Path

from PIL import Image

from .common import ACCENT, EXTRA
from .geometry import chord_through, cn, heading, right_angle_mark, star_at

THREEB_DIR = Path(__file__).parent / "3b1b"
# 裁出播放器画面本身（16:9），去掉浏览器页面背景和左右留白。
SUMMARY_FRAMES = [
    ("3b1b", 57, 809, 5, 1342),
    ("sub0", 65, 816, 3, 1339),
    ("sub1", 63, 815, 4, 1341),
    ("sub2", 57, 809, 2, 1334),
]

SUMMARY_STEPS = [
    ("① 三维点光源用面受光，亮度与距离平方成反比", r"B\propto\frac{1}{r^{2}}"),
    ("② 反勾股定理：一盏灯换成两盏等效灯", r"\frac{1}{h^{2}}=\frac{1}{a^{2}}+\frac{1}{b^{2}}"),
    (
        "③ 半径倍增与等效替换，极限下得到奇数项之和",
        r"1+\frac{1}{3^{2}}+\frac{1}{5^{2}}+\frac{1}{7^{2}}+\cdots=\frac{\pi^{2}}{8}",
    ),
    ("④ 代数运算得到最初要求的表达式", r"S=\frac{\pi^{2}}{8}\cdot\frac{1}{1-\frac{1}{4}}=\frac{\pi^{2}}{6}"),
]


def player_frame(name: str, top: int, bottom: int, left: int, right: int) -> ImageMobject:
    """裁出 scenes/3b1b 截图里的播放器画面。"""
    array = np.asarray(Image.open(THREEB_DIR / f"{name}.png").convert("RGB"))
    return ImageMobject(array[top:bottom, left:right])


def mini_inverse_pythagoras() -> VGroup:
    """几何章屏幕 2 的缩略图：斜边上的高 h 与两条直角边 a、b。"""
    A = LEFT * 0.55 + DOWN * 0.25
    B = RIGHT * 0.42 + DOWN * 0.25
    H = LEFT * 0.05 + DOWN * 0.25
    C = LEFT * 0.05 + DOWN * 0.25 + UP * np.sqrt((H[0] - A[0]) * (B[0] - H[0]))
    return VGroup(
        Polygon(A, B, C, color=WHITE, stroke_width=2, fill_opacity=0.05),
        Line(C, H, color=ACCENT, stroke_width=2),
        right_angle_mark(C, A, B, 0.09),
        right_angle_mark(H, C, B, 0.07),
    )


def mini_lamp_switch() -> VGroup:
    """几何章屏幕 3 的缩略图：小圆上的一盏灯换成大圆上的两盏等效灯。"""
    P = DOWN * 0.31
    r1, r2 = 0.15, 0.3
    O1, O2 = P + UP * r1, P + UP * r2

    phi = np.deg2rad(115)
    R = O1 + RIGHT * r1 * np.sin(phi) + DOWN * r1 * np.cos(phi)
    normal = np.array([-(R - P)[1], (R - P)[0], 0.0])
    S1, S2 = sorted(chord_through(R, normal, O2, r2), key=lambda p: -p[0])
    return VGroup(
        Circle(radius=r1, color=WHITE, stroke_width=2).move_to(O1),
        Circle(radius=r2, color=WHITE, stroke_width=2).move_to(O2),
        DashedLine(S2, S1, color=WHITE, stroke_width=1.5, stroke_opacity=0.6),
        Line(P, S1, color=WHITE, stroke_width=1.5, stroke_opacity=0.6),
        Line(P, S2, color=WHITE, stroke_width=1.5, stroke_opacity=0.6),
        star_at(R, radius=0.03),
        star_at(S1, radius=0.028),
        star_at(S2, radius=0.028),
    )


class BaselGeometrySummary(Scene):
    """屏幕 1：四步串起几何路线，末尾用参考截图盖住总结。"""

    def build_steps(self) -> VGroup:
        minis = {"②": mini_inverse_pythagoras, "③": mini_lamp_switch}
        steps = VGroup()
        for text, formula in SUMMARY_STEPS:
            line = MathTex(formula).scale(0.52)
            if text[0] in minis:
                line = VGroup(line, minis[text[0]]()).arrange(RIGHT, buff=0.3)
            steps.add(VGroup(cn(text, 0.36), line).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        steps.move_to(DOWN * 0.3)
        return steps

    def framed(self, spec: tuple) -> Group:
        picture = player_frame(*spec[:5]).set_width(spec[5])
        border = SurroundingRectangle(
            picture, color=WHITE, stroke_width=1.5, stroke_opacity=0.45, buff=0.0
        )
        return Group(picture, border)

    def build_pictures(self) -> tuple[Group, Group]:
        big = self.framed((*SUMMARY_FRAMES[0], 8.2))
        big.move_to(DOWN * 0.3)
        smalls = Group(*[self.framed((*row, 4.0)) for row in SUMMARY_FRAMES[1:]])
        smalls.arrange(RIGHT, aligned_edge=DOWN, buff=0.2)
        smalls.move_to(DOWN * 2.2)
        return big, smalls

    def construct(self):
        title = heading("几何方法总结", "Wästlund 的证明 · 四步")
        steps = self.build_steps()
        big, smalls = self.build_pictures()

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.8)
        self.wait(2.2)

        self.play(FadeIn(steps[0][0]), run_time=0.6)
        self.wait(3.4)
        self.play(Write(steps[0][1]), run_time=0.9)
        self.wait(1.6)

        self.play(FadeIn(steps[1][0]), run_time=0.6)
        self.play(Write(steps[1][1]), run_time=1.2)
        self.wait(2.4)

        self.play(FadeIn(steps[2][0]), run_time=0.6)
        self.wait(4.0)
        self.play(Write(steps[2][1]), run_time=1.5)
        self.wait(5.35)

        self.play(FadeIn(steps[3][0]), run_time=0.6)
        self.wait(2.55)
        self.play(Write(steps[3][1]), run_time=1.2)
        self.wait(2.0)
        self.play(steps[3][1].animate.set_color(ACCENT), run_time=0.7)
        self.wait(2.05)

        self.play(FadeIn(big), run_time=1.4)
        self.wait(2.65)
        self.play(
            LaggedStart(*[FadeIn(picture) for picture in smalls], lag_ratio=0.35),
            run_time=2.6,
        )
        self.wait(2.3)


class BaselGeometryQuestion(Scene):
    """屏幕 2：几何、奇数项和、代数收尾、要求的长表达式排成一条线。"""

    def build_geometry(self) -> VGroup:
        block = VGroup(
            cn("几何：圆与灯", 0.42), mini_lamp_switch().scale(1.8)
        ).arrange(DOWN, buff=0.2)
        return block

    def build_odd_sum(self) -> VGroup:
        block = VGroup(
            cn("几何得到", 0.42),
            MathTex(r"1+\frac{1}{3^{2}}+\frac{1}{5^{2}}+\cdots=\frac{\pi^{2}}{8}").scale(0.55),
        ).arrange(DOWN, buff=0.2)
        return block

    def build_algebra(self) -> VGroup:
        block = VGroup(
            cn("代数收尾", 0.42),
            MathTex(r"\frac{3}{4}S=\frac{\pi^{2}}{8}").scale(0.72),
            MathTex(r"S=\frac{\pi^{2}}{6}").scale(0.72),
        ).arrange(DOWN, buff=0.16)
        box = SurroundingRectangle(block, color=WHITE, buff=0.22, stroke_width=2)
        box.set_stroke(opacity=0.5)
        box.set_fill(opacity=0)
        return VGroup(block, box)

    def build_result(self) -> VGroup:
        block = VGroup(
            cn("要求的表达式", 0.42),
            MathTex(r"S=1+\frac{1}{2^{2}}+\frac{1}{3^{2}}+\frac{1}{4^{2}}+\cdots").scale(0.62),
        ).arrange(DOWN, buff=0.2)
        return block

    def construct(self):
        title = heading("一个没被回答的问题", "几何的收尾交给了代数")
        geometry = self.build_geometry()
        odd = self.build_odd_sum()
        algebra = self.build_algebra()
        result = self.build_result()
        row = VGroup(geometry, odd, algebra, result).arrange(
            RIGHT, aligned_edge=UP, buff=0.8
        )
        row.move_to(DOWN * 0.45)

        # 「先求奇数幂次和，再用代数算出 S」这一整段，就是想要绕开的部分。
        detour = VGroup(odd, algebra[0])
        cover = SurroundingRectangle(VGroup(odd, algebra), color=WHITE, buff=0.26)
        cover.set_fill(opacity=0.26)
        cover.set_stroke(width=2, opacity=0.45)

        frame = SurroundingRectangle(geometry, color=WHITE, buff=0.2, stroke_width=2)
        step_note = cn("只是重新整理了一遍", 0.36).set_opacity(0.6)
        step_note.next_to(frame, DOWN, buff=0.3)
        same_note = cn(
            "能搜到的几何方法，都是先得到奇数幂次和，\n再代数计算 S，和 3Blue1Brown 完全一样",
            0.34,
        ).set_opacity(0.6)
        same_note.move_to(DOWN * 2.95)
        doubt = MathTex("?").scale(1.6).set_color(ACCENT)
        doubt.move_to(algebra[1].get_corner(UL) + LEFT * 0.3 + UP * 0.1)
        line_y = odd[1].get_center()[1]
        box_left, box_right = algebra[1].get_left()[0], algebra[1].get_right()[0]
        to_odd = Arrow(
            (frame.get_right()[0], line_y, 0.0),
            (odd[1].get_left()[0], line_y, 0.0),
            buff=0.1,
            stroke_width=3,
            max_stroke_width_to_length_ratio=8,
        )
        into_algebra = Arrow(
            (odd[1].get_right()[0], line_y, 0.0),
            (box_left, line_y, 0.0),
            buff=0.1,
            stroke_width=3,
            max_stroke_width_to_length_ratio=8,
        )
        out_of_algebra = Arrow(
            (box_right, line_y, 0.0),
            (result[1].get_left()[0], line_y, 0.0),
            buff=0.1,
            stroke_width=3,
            max_stroke_width_to_length_ratio=8,
        )
        bypass = Arrow(
            frame.get_top() + UP * 0.1,
            result.get_top() + UP * 0.1,
            color=ACCENT,
            buff=0.2,
            path_arc=-0.5,
            stroke_width=4,
            max_stroke_width_to_length_ratio=8,
        )
        bypass_label = cn("不能直接从几何得到吗？", 0.44).set_color(ACCENT)
        bypass_label.move_to(UP * 2.2)

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.9)
        self.wait(1.92)

        self.play(FadeIn(geometry), Create(frame), run_time=1.2)
        self.wait(4.48)

        self.play(FadeIn(step_note), run_time=0.7)
        self.wait(2.73)

        self.play(frame.animate.set_color(ACCENT), run_time=0.8)
        self.play(FadeIn(odd), Create(to_odd), run_time=1.1)
        self.wait(2.68)

        self.play(
            FadeIn(algebra),
            FadeIn(result),
            Create(into_algebra),
            Create(out_of_algebra),
            run_time=1.6,
        )
        self.wait(1.27)

        self.play(FadeIn(same_note), run_time=0.9)
        self.wait(4.52)

        self.play(FadeIn(doubt), run_time=0.7)
        self.wait(3.39)

        self.play(
            detour.animate.set_opacity(0.3),
            algebra[1].animate.set_stroke(opacity=0.25),
            FadeIn(cover),
            Create(bypass),
            FadeIn(bypass_label),
            run_time=1.8,
        )
        self.wait(3.0)


class BaselGeometryDirect(Scene):
    """屏幕 3：每翻一倍只在正对面补一盏灯，极限下整数点全是灯。"""

    STAGES = 5
    R0 = 0.14
    STEP = 0.38
    NOTE_AT = LEFT * 4.2 + UP * 2.35

    def note(self, text: str):
        return cn(text, 0.42).move_to(self.NOTE_AT)

    def build_lamps(self) -> tuple:
        P = LEFT * 4.6 + DOWN * 3.0
        circles, kids, added, chords = VGroup(), VGroup(), VGroup(), VGroup()
        layers = []
        for k in range(self.STAGES):
            radius = self.R0 * 2**k
            center = P + UP * radius
            circles.add(Circle(radius=radius, color=WHITE, stroke_width=2.2).move_to(center))
            antipode = center + UP * radius
            pts = []
            for s in range(1, 2 ** (k + 1)):
                if s == 2**k:
                    continue
                theta = -np.pi / 2 + np.pi * s / 2**k
                pts.append(center + radius * np.array([np.cos(theta), np.sin(theta), 0.0]))
            layers.append(pts + [antipode])
            kids.add(VGroup(*[star_at(pt, radius=0.045) for pt in pts]))
            added.add(star_at(antipode, color=EXTRA, radius=0.06))
        for k in range(self.STAGES - 1):
            radius = self.R0 * 2 ** (k + 1)
            center = P + UP * radius
            group = VGroup()
            for point in layers[k]:
                direction = np.array([-(point - P)[1], (point - P)[0], 0.0])
                a, b = chord_through(point, direction, center, radius)
                group.add(Line(a, b, color=WHITE, stroke_width=1.2, stroke_opacity=0.35))
            chords.add(group)
        guide = DashedLine(
            P,
            P + UP * (2 * self.R0 * 2 ** (self.STAGES - 1)),
            stroke_width=1.4,
            stroke_opacity=0.45,
        )
        return P, circles, kids, added, chords, guide
    def build_ledger(self) -> tuple:
        caption = cn("每盏新灯给总亮度加上", 0.4)
        terms = VGroup(
            MathTex(r"\frac{\pi^2}{2^2}"),
            MathTex(r"+\ \frac{\pi^2}{4^2}"),
            MathTex(r"+\ \frac{\pi^2}{8^2}"),
            MathTex(r"+\ \frac{\pi^2}{16^2}"),
            MathTex(r"+\ \frac{\pi^2}{32^2}"),
            MathTex(r"+\ \cdots"),
        )
        for term in terms:
            term.scale(0.5).set_color(EXTRA)
        terms.arrange(RIGHT, buff=0.08)
        ledger = VGroup(caption, terms).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        return ledger, caption, terms

    def build_line(self) -> VGroup:
        offsets = [v for v in range(-7, 8) if v]
        line = Line(LEFT * 3.15, RIGHT * 3.15, color=WHITE, stroke_width=2)
        dot = Dot(radius=0.05, color=WHITE)
        origin = VGroup(dot, MathTex("P").scale(0.44).next_to(dot, UP, buff=0.12))
        lamps = VGroup(*[star_at(RIGHT * self.STEP * v, radius=0.05) for v in offsets])
        labels = VGroup(
            *[
                MathTex(str(v)).scale(0.36).next_to(RIGHT * self.STEP * v, DOWN, buff=0.16)
                for v in offsets
            ]
        )
        return VGroup(line, origin, lamps, labels)

    def build_formula(self) -> tuple:
        read = MathTex(
            r"S=\frac{1}{2}\left(\frac{\pi^2}{2^2}+\frac{\pi^2}{4^2}+\frac{\pi^2}{8^2}+\cdots\right)"
        ).scale(0.55)
        algebra = VGroup(
            MathTex(r"=\frac{1}{2}\cdot\frac{\pi^2}{4}\cdot\frac{1}{1-\frac{1}{4}}").scale(0.55),
            MathTex(r"=\frac{\pi^2}{6}").scale(0.6),
        ).arrange(RIGHT, buff=0.18)
        return VGroup(read, algebra).arrange(DOWN, aligned_edge=LEFT, buff=0.22), read, algebra

    def construct(self):
        title = heading("直接从几何读出 S", "每翻一倍，只补一盏")
        P, circles, kids, added, chords, guide = self.build_lamps()
        ledger, caption, terms = self.build_ledger()
        line_block = self.build_line()
        formula, read, algebra = self.build_formula()
        line, origin, line_lamps, line_labels = line_block

        notes = [
            self.note("周长 2：弧上间隔 1，一盏灯"),
            self.note("周长 4：在 P 的对面补一盏"),
            self.note("周长 8：同样只补一盏"),
            self.note("周长 16：只补一盏"),
            self.note("周长 32：只补一盏"),
        ]
        note_sum = self.note("每补一盏，总亮度就多一档")
        note_geo = self.note("新灯都在 P 的正对面，距离翻倍")
        note_line = self.note("整数点上全是灯，两侧合起来是 2S")
        note_read = self.note("每一项都从图上读出来")

        lamp_P = Dot(P, radius=0.05, color=WHITE)
        label_P = MathTex("P").scale(0.44).next_to(P, DOWN, buff=0.12)
        two_s = VGroup(
            cn("两侧合起来的总亮度", 0.4), MathTex(r"=2S").scale(0.6)
        ).arrange(RIGHT, buff=0.25)

        column = VGroup(ledger, two_s, line_block, formula).arrange(
            DOWN, aligned_edge=LEFT, buff=0.55
        )
        column.move_to(RIGHT * 3.05 + DOWN * 0.4)
        box = SurroundingRectangle(terms, color=EXTRA, buff=0.12).move_to(terms.get_center())

        self.play(Write(title[0]), FadeIn(title[1]), run_time=0.9)
        self.play(Create(guide), FadeIn(lamp_P), FadeIn(label_P), run_time=0.9)

        # 周长 2：初始那一盏灯，也是亮度表的第一项
        self.wait(2.2)
        self.play(Create(circles[0]), FadeIn(notes[0]), run_time=0.9)
        self.wait(1.3)
        self.play(FadeIn(caption), Write(terms[0]), FadeIn(added[0]), run_time=1.0)

        # 四次翻倍：画新圆时清掉上一轮的辅助线，补灯与右侧新增一项同时出现
        self.wait(1.3)
        self.play(Create(circles[1]), run_time=0.8)
        self.play(
            Create(chords[0]),
            FadeIn(kids[1]),
            FadeOut(notes[0]),
            FadeIn(notes[1]),
            run_time=1.1,
        )
        self.wait(0.9)
        self.play(FadeIn(added[1]), Write(terms[1]), run_time=0.9)
        self.wait(1.8)
        self.play(
            LaggedStart(
                *[Indicate(lamp, scale_factor=1.35) for lamp in kids[1]], lag_ratio=0.3
            ),
            run_time=1.2,
        )

        self.wait(1.4)
        self.play(
            Create(circles[2]),
            Create(chords[1]),
            FadeIn(kids[2]),
            FadeOut(chords[0]),
            FadeOut(notes[1]),
            FadeIn(notes[2]),
            run_time=1.4,
        )
        self.wait(0.4)
        self.play(FadeIn(added[2]), Write(terms[2]), run_time=0.9)
        self.wait(2.3)
        self.play(
            LaggedStart(
                *[Indicate(lamp, scale_factor=1.35) for lamp in kids[2]], lag_ratio=0.1
            ),
            run_time=1.3,
        )

        self.wait(1.9)
        self.play(
            Create(circles[3]),
            Create(chords[2]),
            FadeIn(kids[3]),
            FadeOut(chords[1]),
            FadeOut(notes[2]),
            FadeIn(notes[3]),
            run_time=1.5,
        )
        self.wait(0.8)
        self.play(FadeIn(added[3]), Write(terms[3]), run_time=0.9)

        self.wait(0.5)
        self.play(
            Create(circles[4]),
            Create(chords[3]),
            FadeIn(kids[4]),
            FadeOut(chords[2]),
            FadeOut(notes[3]),
            FadeIn(notes[4]),
            run_time=1.5,
        )
        self.play(FadeIn(added[4]), Write(terms[4]), run_time=0.9)
        self.wait(0.6)

        # 与上一页的分别：这里数的是补上的灯，它们的距离每次翻倍
        self.play(FadeOut(notes[4]), FadeIn(note_sum), run_time=0.9)
        self.wait(1.1)
        self.play(
            LaggedStart(*[Indicate(lamp, scale_factor=1.6) for lamp in added], lag_ratio=0.25),
            run_time=2.6,
        )
        self.wait(1.3)
        self.play(FadeOut(note_sum), FadeIn(note_geo), run_time=1.0)
        self.wait(3.5)
        self.play(Write(terms[5]), Create(box), run_time=1.2)
        self.wait(1.0)

        self.play(
            circles.animate.set_opacity(0.22),
            kids.animate.set_opacity(0.3),
            added.animate.set_opacity(0.45),
            FadeOut(chords[3]),
            run_time=1.5,
        )
        self.wait(1.4)
        self.play(Create(line), FadeIn(origin), run_time=1.3)
        self.play(FadeIn(two_s), run_time=0.8)
        self.wait(1.8)
        self.play(
            LaggedStart(*[FadeIn(lamp) for lamp in line_lamps], lag_ratio=0.05),
            run_time=1.6,
        )
        self.play(FadeIn(line_labels), FadeOut(note_geo), FadeIn(note_line), run_time=1.0)
        self.wait(0.3)
        self.play(Write(read), run_time=1.5)
        self.wait(1.5)

        self.play(Write(algebra), run_time=1.8)
        self.wait(0.6)
        self.play(
            algebra[1].animate.set_color(ACCENT),
            FadeOut(note_line),
            FadeIn(note_read),
            run_time=1.0,
        )
        self.wait(1.6)
