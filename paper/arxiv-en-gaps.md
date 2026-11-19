# 英文版上 arXiv：第三轮（只剩两条要你定）

本轮改动都编译过了，三份产物：中文全内容版 `output/basel_problem_paper.pdf`（7 页）、
中文几何版 `output/basel_problem_paper_geo.pdf`（5 页）、英文版 `output/basel_problem_paper_en.pdf`
（6 页，第 6 页整页是参考文献）。

本轮改动摘要（不需要再确认，列在这里只是好核对）：

| 项目 | 结果 |
| --- | --- |
| AI 署名 | 三版正文都不提；改在仓库 `README.md` 末尾一句说明，并指向 `docs/part_qwen3.8_flash.md`（该文件未改动） |
| 英文版范围 | 只投几何路线，不补收敛性那两句 |
| 先前工作 | 三版引言末尾各加一段 remark，新增 Kalman(1993)/Matsuoka(1961)/Komornik(2022) 三条参考文献 |
| 标题 | 中文全内容版保持《巴塞尔问题》原题不动；几何版中文与英文用「多走一步」+ 副题（英文副题取 `Reading $\sum 1/n^2$ off a Picture`，中文对译「把 $\sum 1/n^2$ 直接从图上读出来」） |
| 关键词 | 五个：`Basel problem; geometric proof; inverse-square law; inverse Pythagorean theorem; Wästlund's construction`（中文同） |
| figure 4 | `scale` 0.55 → 0.8，三版同步；几何版中文的参考文献整段套了 `\small`，好让五条留在第 5 页内、不产生只有两行的孤立页 |
| 中文全内容版的引用 | Euler/Ahlfors/Apostol 三条已补上 `\cite`（第 3、4 节用得到），共 8 条 |
| 仓库/视频链接 | 不进正文 |
| 单位 | 只留邮箱，不写邮政地址 |

下面两条是我不能替你决定的。

---

## 1. 要不要给 Wästlund 发一封邮件

你上一轮反问「和他通信的用处是什么」，我的答复：**用处不大，但不是零**。

- 你的正文归属已经写清了（引言一句 + 致谢一句），arXiv 的 math.HO 没有编辑审这一层，
  所以「不通信」不会带来任何流程上的障碍。
- 唯一的风险是：有人知道他这篇 2010 年的短文，看到「补一盏灯」会想「作者本人是不是早就说过」。
  一句 `I thank the author for confirming ...` 或 `... for his reply` 能把这个疑问一次性关掉；
  没有通信时，这个疑问只能靠读者自己读你的 §3 来判断——而 §3 写得足够自洽，所以问题不大。
- 实际收益取决于他是否回复。这文章放了 15 年、未刊、作者已转向其它方向，不回复的概率不低。

所以：

- [ ] A. **不发**，保持现状——建议（正文已经足够清楚）
- [ ] B. 发一封两句话的邮件告知（不要求回复，只是留个痕迹）；若他回了，再在致谢里加一句
- [ ] C. 现在就先写 `after correspondence with the author`（**不建议**，写了就得真有）

待填：`____`

## 2. arXiv 主分类

你上一轮说「看 Wästlund 那篇文章的分类吧，应该是一致的」——**照不到**：他的 `Cosmic.pdf`
不在 arXiv 上（他名下 23 条 arXiv 记录里没有 Basel 相关），PDF 首页也没有 MSC 码。
所以主分类只能自己定，我的建议：

- 主 `math.HO`（History and Mathematics；科普型短文、单页几何证明常走这里，
  你这篇的写法——灯、亮度、一张图讲完——正是 HO 的口味）
- cross-list `math.MG`（与 MSC 51M04 对得上，能被几何方向检索到）+ `math.NT`（ζ(2) 的人也会搜到）

- [ ] A. 按上面这样：主 HO，cross MG + NT——建议
- [ ] B. 主 `math.MG`，cross HO + NT（更想被几何的人看到）
- [ ] C. 只提一个分类，不 cross-list

待填：`____`

---

## 提交当天要填的表单项（不用写进 PDF，记一下）

- 许可：**arXiv non-exclusive distribution**（你上一轮已确认）。
- **endorsement**：新账号投 math.* 通常要背书人。走 auto-endorse 就行，但会多等一两天；
  若被要求填背书人，需要一位已有 arXiv 发布记录的 math.* 作者邮箱。
- `comments` 栏（只显示在 abstract 页，不进 PDF）：可以写 `6 pages, 4 figures`，
  等仓库/视频公开后再补一版写 URL。

填完这两条，清单里就只留结果不留问题了。
