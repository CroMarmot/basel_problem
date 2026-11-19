# 英文版上 arXiv：第二轮确认

上一轮 7 项已经落到 PDF 里，不用再填：

| 项目 | 结果 |
| --- | --- |
| 英文标题 | `One More Step on Wästlund's Geometric Proof of the Basel Problem` |
| 作者/单位/邮箱 | YeXiaoRain，Independent researcher, Chengdu, Sichuan, China，yexiaorain@gmail.com（写在 `\thanks`） |
| 日期 | 两版都写死 2026-11-20 |
| 摘要 | 按「在 Wästlund 的几何构造上多走一步」重写，明说新结果 |
| MSC 2020 | 主 51M04；次 40A05、11A25、01A50 |
| 引言预告贡献 | 已写：Wästlund 是方法提供者，本文只去掉收尾那段代数 |
| 定理结构 | Theorem 1.1（Wästlund，奇数项和）+ Theorem 1.2（本文，直接读出 $S$）分两条 |
| 定理环境 | Definition 2.1（灯/亮度/等效/正对面）、Lemma 2.1–2.3、Lemma 3.1、Proposition 3.2，各配 `proof` |
| 归属声明 | 引言里一句 + 文末 Acknowledgments 谢 Wästlund 与 3Blue1Brown |
| 参考文献 | 只留 Wästlund 与 3Blue1Brown，两条都带日期与 URL；Euler/Ahlfors/Apostol 已删 |
| 图注 | 其余三张图不加长说明，只有一张图的静图有一句题注 |
| 目录 | 英文版不放 |
| 引擎 | 英文版 `paper_en/build.py` 走 pdfLaTeX，5 页 A4，无未定义引用；中文版 7 页，缺字检查通过 |

Wästlund 那条我按他 PDF 首页核对过著录信息：题名是小写的 `Summing inverse squares by euclidean geometry`，
Chalmers，2010-12-08；arXiv 上检索不到这一篇（他名下 23 条里没有 Basel 相关），所以只能引 Chalmers 的 URL，
条目里标了 `Unpublished note`。3Blue1Brown 按 YouTube 页面写 2018-03-03（发表日，不是访问日）。

下面是还需要你点头的东西。空着不填的按「建议」那行处理。

---

## 1. 作者栏要不要出现 AI（唯一一条我不能替你决定的）

上一轮你写「Qwen3.8-Flash 也加上」，**这条我没做**：arXiv 的作者栏要求自然人，
署 AI 名会直接卡住提交，也可能被判定为不合规。三个选项：

- [ ] A. 作者栏不动，Acknowledgments 里加一句「本文的排版与英文改写借助了 AI 助手」——**建议**
- [ ] B. 完全不提
- [ ] C. 仍然坚持署名（那我照做，但投稿大概率要退回重写）

待填：`___`

## 2. 英文版范围：收敛性 / 欧拉乘积 / 傅里叶 到底留不留

现在英文版**只有几何路线**（Wästlund 综述 + 补灯一步），5 页，标题也对得上。
你上一轮说「那些辅助介绍的无关部分可能在正式版中去掉」。

- [ ] A. 就这样，只投几何——**建议**（标题、摘要、正文自洽，篇幅像一篇 note）
- [ ] B. 把三节也译出来，英文版变「三种证明的综述」，标题要改回更泛的说法

待填：`___`

如果选 A：英文版现在**没有任何收敛性论证**，$\sum 1/n^2$ 的绝对收敛是按 Wästlund 原文默认事实用的。
要不要补一句（两行，不新开一节）？

- [ ] 补一句「级数显然收敛」+ 与 $\sum 1/n(n-1)$ 比较的裂项一行——**建议补**
- [ ] 不补

## 3. 先前工作的引用（审稿最容易挑的一点）

几何路线上,Wästlund 不是第一个把 $\pi^2/6$ 和几何扯上关系的人。最常被提到的是
Yaglom & Yaglom《Challenging Mathematical Problems with Elementary Solutions》(1953/1964)
里那个用折线投影/正弦乘积的初等推导。它和本文构造**不同**,但不提一句容易被认为不知晓。

- [ ] A. 引言末尾加 2–3 句 remark（承认更早的初等/几何推导存在，说明本文只针对 Wästlund 这一支）——**建议**
- [ ] B. 不加，保持只有两条参考文献

待填：`___`（若选 A，还要不要顺手加 Apostol 或 Kalman 的 $\zeta(2)$ 综述作「更多证明见」？）

## 4. 是否已与 Wästlund 本人通信

归属声明现在写的是「§2 复述 Wästlund，§3 是本文的观察」，没提通信。
如果你邮件问过他、或打算问，加一句「after correspondence with the author」会显著降低原创性质疑。

待填：`___`（没有就写「无通信」，我保持现状）

## 5. arXiv 分类与许可（表单要填，我先给建议）

- 主分类：`math.HO`（Mathematics Education / Overview，科普型短文常走这里）还是 `math.MG`（Metric Geometry，
  与 MSC 51M04 更对得上）——建议 **主 math.HO，cross-list math.MG + math.NT**。
  你若希望被几何方向的人检索到，就把 MG 提为主。
  - 待填：`___`
- 许可：**arXiv non-exclusive distribution**（最省事）还是 CC BY 4.0（利于视频/公众号转载注明来源）——建议 non-exclusive。
  - 待填：`___`
- 提醒：新账号投 math.* 通常要 endorsement，arXiv 会让你填一位背书人邮箱或走 auto-endorse。

## 6. GitHub 仓库 / YouTube 链接放不放正文

你问的这条我的答复是：**不建议放在正文**（URL 不稳定，arXiv 也不喜欢正文里的营销性外链，
且投稿版和公开版之间不能出现无法核验的外部依赖）。三种可行位置：

- [ ] A. 都不放，等 arXiv 编号下来后写进「仓库 README」和视频简介——**建议**
- [ ] B. 放脚注，写作「animations and source: \url{...}」，接受链接可能变
- [ ] C. 放 arXiv 表单的 `comments` 栏（不进 PDF，只在 abstract 页显示）

待填：`___`（要放的话给我最终仓库 URL，视频发布后再补一次版本）

## 7. 措辞层面顺手确认的小事

- 单位写法 `Independent researcher, Chengdu, Sichuan, China`：arXiv 对独立研究者一般不卡,
  但有时会要求通信地址；要不要在 `\thanks` 里只留邮箱（现状）还是补一个邮政地址？
  - 待填：`___`
- 英文副标题：现在**没有**副标题（你上一轮说没想好）。我建议不加——主标题已经说清了做了什么。
  要加的话备选：`A one-lamp-per-round modification`、`Reading $\sum 1/n^2$ off a picture`。
  - 待填：`___`
- 中文标题：要不要跟着改成《巴塞尔问题：在 Wästlund 的几何证明上多走一步》（现在是《巴塞尔问题》+ 副题）？
  - 待填：`___`
- 中文版要不要在摘要下面附一段**英文标题 + 英文摘要**（中文期刊体例常见，arXiv 不需要）？
  - 待填：`___`
- 关键词五个：`Basel problem; Euclidean geometry; inverse-square law; inverse Pythagorean theorem; Wästlund`。
  要不要把 `inverse Pythagorean theorem` 换成 `$\zeta(2)$`？
  - 待填：`___`
- 中文版参考文献里 Euler / Ahlfors / Apostol 三条从没被 `\cite` 过（英文版已删）。
  中文版是**删掉**还是**补上引用**？（第 3、4 节确实用得到 Euler 与 Apostol）
  - 待填：`___`

---

填完发我，我按选择改 `paper_en/` 与 `paper/`，两版重新编译；改完这份清单只留结果不留问题。
