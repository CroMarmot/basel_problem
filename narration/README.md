# 语音原稿

这里的 `.md` 文件是**逐字送进 Edge TTS 的原稿**，不是给人读的说明。
「这一屏讲什么、画什么、怎么对齐」的规范仍然只在根目录的 `specs.md`；
本目录只负责「具体说出来的那句话」。

## 目录结构

```
narration/
  zh/            # 中文原稿，默认版本
    intro.md     # 一个章节一个文件，文件名 = scenes/__init__.py 里的章节 key
    ...
  en/            # 英文原稿，结构与 zh/ 逐节对应（--lang en 使用）
```

文件内用 `## <子片段 key>` 分节，节名必须与 `scenes/__init__.py` 的 `SCENES` /
`CHAPTERS` 中的子片段 key 一致；正文就是该子片段的旁白，段落之间不要插入别的说明文字，
说明一律写进 HTML 注释。

## 同音替字（勿改回）

Edge TTS 会把个别汉字的常用读音读错，所以原稿里用**只有正确读音的同音字**替换，
这不是错别字，未来「修 typo」时请勿顺手改回：

| 原稿写法 | 实际用字 | 原因 |
| --- | --- | --- |
| 鸡数项、正负鸡数 | 奇数 | 「奇」会被读成 qí，正确读音 jī |
| 药求 | 要求 | 「要」在「要求」里会被读成 yāo，正确读音 yào |
| 倒树 | 倒数 | 「数」在「倒数」里会被读成 shǔ（倒数的动词读法），正确读音 shù |

英文稿不受影响；`specs.md` 与论文里一律写规范用字，替字只存在于 `narration/zh/`。

## 英文稿的写法

`narration/en/` 是中文稿的 1:1 对译：逐句翻译，不增不减，小节 key 与中文完全一致，
这样 `--list` 与 `--lang en` 能走同一套章节/片段逻辑。两条注意：

- 不要把中文里的同音替字带进英文（那是 TTS 的读法补丁，只对中文生效）。
- 屏幕上原本以英文出现的字（公式、`Wästlund` 之类）原样保留；中文主标题的英文副标题
  在英文版里是重复信息，已在 `scenes/i18n.py` 里置 `None` 去掉。

英文配音统一用 `en-US-AriaNeural`、rate `+8%`（`basel_problem.py` 的 `VOICES` / `TTS_RATES`）。

## 改稿之后

```
.venv/bin/python ./basel_problem.py --segments geometry_result
.venv/bin/python ./basel_problem.py --lang en --segments geometry_result
```

产物按内容指纹复用：旁白一个字没改就直接用目录里现成的 `<片段名>-<ahash>.mp3`，
改了就重新配音并换名，无声视频照用。视频需要比旁白略长（0.5–1.1s 余量），
所以中文改完旁白通常还要同步调 `scenes/` 里对应的 `self.wait()` 节拍；
英文版不动画面，靠配音 rate 和合并时的定格补齐。
