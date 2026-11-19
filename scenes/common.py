from manim import TEAL, UP, WHITE, YELLOW, Text, VGroup

CN_FONT = "Noto Sans CJK SC"
ACCENT = YELLOW
# 只在需要区分「原有的」和「新补上的」两类对象的画面上使用。
EXTRA = TEAL


def cn(text: str, scale: float = 0.55, color=WHITE) -> Text:
    return Text(text, font=CN_FONT, color=color).scale(scale)


# 全片统一的标题块：主标题 scale 0.8、副标题 22pt×0.42，两者都水平居中，
# 居中点固定在下面这两个高度上，正文一律排在副标题下方。
TITLE_AT = UP * 3.35
SUBTITLE_AT = UP * 2.85
# 辅助性正文的基础字号：不许超过主标题，公式（MathTex）按版面需要可以更大。
BODY_SCALE = 0.5


def body(text: str) -> Text:
    return cn(text, BODY_SCALE)


def screen_title(title_text: str, subtitle_text: str = "", mark: str = "") -> VGroup:
    """mark 单独染成黄色缀在主标题末尾（007 用它把「？」换成「✓」）。"""
    colored = {"t2c": {mark: ACCENT}} if mark else {}
    title = Text(title_text + mark, font=CN_FONT, color=WHITE, **colored).scale(0.8)
    title.move_to(TITLE_AT)
    if not subtitle_text:
        return VGroup(title)
    subtitle = Text(subtitle_text, font=CN_FONT, font_size=22).scale(0.42)
    subtitle.move_to(SUBTITLE_AT)
    return VGroup(title, subtitle)
