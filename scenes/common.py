import os

from manim import TEAL, UP, WHITE, YELLOW, Text, VGroup

from .i18n import has_cjk, translate

CN_FONT = "Noto Sans CJK SC"
ACCENT = YELLOW
# 只在需要区分「原有的」和「新补上的」两类对象的画面上使用。
EXTRA = TEAL

# 成片语言。`BASEL_LANG=en` 时屏幕文字一律走 scenes/i18n.py 的英文对译，
# 缺译会在构建时直接失败；旁白原稿同步切到 narration/en/。
# 读的是环境变量，而且是每次调用时读——入口脚本在 import 完场景之后才设这个变量。
def lang() -> str:
    return os.environ.get("BASEL_LANG", "zh")


# 英文比中文宽得多，单条文字超过这个宽度就等比缩到刚好放得下（14.2 的画幅留两侧余量）。
MAX_TEXT_WIDTH = 12.4


def show(text: str) -> str | None:
    if lang() == "zh":
        return text
    return translate(text)


def _label(text: str, scale: float, color) -> Text:
    """按当前语言造一条文字；英文缺译时 translate 会终止构建。"""
    shown = show(text)
    if shown is None:
        return Text("", font=CN_FONT)
    label = Text(shown, font=CN_FONT, color=color).scale(scale)
    if lang() == "en" and label.width > MAX_TEXT_WIDTH:
        label.scale(MAX_TEXT_WIDTH / label.width)
    return label


def cn(text: str, scale: float = 0.55, color=WHITE) -> Text:
    return _label(text, scale, color)


# 全片统一的标题块：主标题 scale 0.8、副标题 22pt×0.42，两者都水平居中，
# 居中点固定在下面这两个高度上，正文一律排在副标题下方。
TITLE_AT = UP * 3.35
SUBTITLE_AT = UP * 2.85
# 辅助性正文的基础字号：不许超过主标题，公式（MathTex）按版面需要可以更大。
BODY_SCALE = 0.5


def body(text: str) -> Text:
    return cn(text, BODY_SCALE)


def screen_title(title_text: str, subtitle_text: str = "", mark: str = "") -> VGroup:
    """mark 单独染成黄色缀在主标题末尾（007 用它把「？」换成「✓」）。

    有些副标题写的就是主标题的英文（「巴塞尔问题」/「Basel Problem」），
    英文成片里这种副标题直接去掉，不然就是主标题的自我重复。
    去掉时留一条空文字占位，场景里 `title[1]` 和「正文排在副标题下方」的定位都不必改。
    """
    title_text = show(title_text) or ""
    mark = show(mark) or ""
    colored = {"t2c": {mark: ACCENT}} if mark else {}
    title = Text(title_text + mark, font=CN_FONT, color=WHITE, **colored).scale(0.8)
    if lang() == "en" and title.width > MAX_TEXT_WIDTH:
        title.scale(MAX_TEXT_WIDTH / title.width)
    title.move_to(TITLE_AT)
    if not subtitle_text:
        return VGroup(title)
    subtitle = show(subtitle_text)
    if subtitle is None or (lang() == "en" and not has_cjk(subtitle_text)):
        return VGroup(title, Text("", font=CN_FONT).move_to(SUBTITLE_AT))
    subtitle = Text(subtitle, font=CN_FONT, font_size=22).scale(0.42)
    if lang() == "en" and subtitle.width > MAX_TEXT_WIDTH:
        subtitle.scale(MAX_TEXT_WIDTH / subtitle.width)
    subtitle.move_to(SUBTITLE_AT)
    return VGroup(title, subtitle)
