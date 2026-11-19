<!--
本文件是 Edge TTS 的英文逐字原稿：## 小节的标题是子片段名，正文原样送进语音合成。
「讲什么、怎么画」的约定在 specs.md，这里只管「具体怎么说」。
英文稿是 narration/zh/ 的 1:1 对译，不使用同音替字（替字只存在于中文稿）。
-->

# Chapter 7 summary

## geometry_summary

Let's string this geometric route together at the end. A point source of light in three dimensions, received by a small surface: the brightness is inversely proportional to the square of the distance. The inverse Pythagorean theorem swaps one lamp for two equivalent lamps. Double the radius again and again and this equivalence keeps holding; in the limit the circle flattens into a straight line, the lamps land on the positive and negative odd integers, and we get the sum of the odd terms. All that is left is algebra: the even terms are exactly a quarter of it, and put together they give the expression we wanted. This geometric route comes from Wästlund, and the popular version comes from 3Blue1Brown.

## geometry_question

But stopping here would only be tidying up someone else's proof, and that is not really the reason for this video. What made me want to make it is that this geometric method is beautiful, yet its ending leans on quite a bit of algebra. And every follow-up video I could find online stays on this same route. Does nobody feel a little uneasy, a little itchy, wanting an expression that comes straight out of the geometry?

## geometry_direct

Look back at the repeated doubling of the circle. We still start with a circle of circumference 2, carrying one lamp every unit of arc. Then double it to a circle of circumference 4: if we add one lamp on the far side of P, this circle can also carry one lamp every unit of arc. Double again, and it turns out that once more a single lamp added at the far side is enough to keep one lamp on every arc of length 1. The same for the circle of circumference 16, the same again for circumference 32. The difference from before is that the total brightness now grows as we keep adding lamps; but the special thing here is that the distance of each newly added lamp doubles every round, so these additions form a geometric series as well. So the figure itself gives us the expression we are after as the sum of a geometric series. The algebra here looks the same as before, only now every single term is read straight off the picture.

## geometry_onepic

Finally, the whole route gathered into one picture. Every time the circle doubles, add one lamp directly opposite P. After doubling the circumference without end, the circle flattens into the line through P, and every integer point carries a lamp. That gives S directly from the geometry as a geometric series, and so the answer.

## geometry_refs

And two reference links to close. The first is Wästlund's original geometric proof. The second is the 3Blue1Brown explainer video.
