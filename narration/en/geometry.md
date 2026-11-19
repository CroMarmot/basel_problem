<!--
本文件是 Edge TTS 的英文逐字原稿：## 小节的标题是子片段名，正文原样送进语音合成。
「讲什么、怎么画」的约定在 specs.md，这里只管「具体怎么说」。
英文稿是 narration/zh/ 的 1:1 对译，不使用同音替字（替字只存在于中文稿）。
-->

# Chapter 6 geometry

## geometry_light

The heart of the geometric proof is to read the inverse square law as brightness: double the distance, and the same light spreads over four times the area, so only a quarter of the brightness is left.

## geometry_pythagoras

In a right triangle the height drawn to the hypotenuse satisfies the inverse Pythagorean theorem: the reciprocal of h, squared, equals the sum of the reciprocals of the two legs, squared.

## geometry_circle

Wästlund moves this step onto circles. There is a point R on the small circle, and the observer at the tangent point P receives its light. Double the radius and draw the large circle tangent to the first one at P. Now through R draw the line perpendicular to RP; it meets the large circle at S1 and S2, and this perpendicular happens to pass through the center of the large circle. This is exactly the setting that the light and the inverse Pythagorean theorem ask for. In other words, the brightness of one lamp on the small circle can be replaced by the equivalent brightness of two lamps on the large circle.

## geometry_doubling

Take the four lamps at the quartering points of the small circle and apply the previous step to all of them at once; eight lamps come out. Look at the angles converging at this center: for the small circle they are inscribed angles, equal in pairs, while for the large circle they are central angles, also equal in pairs. So the N division points on the small circle turn into the corresponding 2N division points on the large circle, with equivalent brightness.

## geometry_limit

We start with a circle of circumference 2, whose single lamp sits directly opposite P, and the brightness is then pi squared over four. Now use the doubling from the last section again and again: circumference and number of lamps double together, while the total brightness stays the same. As the radius tends to infinity, the circle near P looks more and more like a straight line, and chord lengths tend to arc lengths. Put P at the origin, and the lamps land on the positive and negative odd integers, which gives the identity below.

## geometry_result

We now have the sum of the odd terms, pi squared over eight. Next write out the series S that we are after. The even terms left over are obtained by multiplying S by one quarter. Odd terms plus even terms are exactly S, so the answer we want falls out of a short calculation.
