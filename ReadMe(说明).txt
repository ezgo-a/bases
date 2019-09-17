——————This is an constructor of a music game named "Rhythm Master" (Tencent) ———————— 

Contact:   ezgo_transfer@foxmail.com
	
	QQ: 2755703143

——————————————————————————————————————————————

将bases, parameters, extension1 放入一个文件夹。

下载prefix.imd, drawing.mp3放入一个文件夹，把parameters.py的prefix_path改成

prefix.imd, drawing.mp3所在的文件夹。

使用： D点， H线， T折线， B模块。 draw(rm_obj)在IVM上画出(需要安装IVM支持draw()函数）。
例如 
from extension1 import *

a = D(300)
draw(a)

b = H(300, 1000)
draw(b)

c = T([300, 500,900], [-1, 1, 0])
draw(c)
draw(c.mr())

d = B([b,c], ['p', 2])
draw(d)
draw(d.mr())

e = retiming(d, 1000)
draw(e)

f = vibro('12dd1', 300, 3000)
draw(f)

g = gliss('10d1, 300, 2000)
draw(g)
