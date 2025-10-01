from stanfordTeapot import teapot

xmin =0
xmax=0
ymin =0
ymax=0
zmin =0
zmax=0

for i in range(3644):
    x=teapot[i*3]
    y=teapot[i*3+1]
    z=teapot[i*3+2]
    if x < xmin: xmin = x
    if x > xmax: xmax = x
    if y < ymin: ymin = y
    if y > ymax: ymax = y
    if z < zmin: zmin = z
    if z > zmax: zmax = z
print(xmin, xmax, ymin, ymax, zmin, zmax)