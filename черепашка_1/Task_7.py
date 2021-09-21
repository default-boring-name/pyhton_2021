import turtle as trl

trl.speed(0)
 
trl.shape('turtle')
n = 50
N = 5
R = 100
dr = R / (5 * n)
dphi = 6.28 / n
r = dr

trl.penup()
trl.goto(r, 0)
trl.setheading(90)
trl.pendown()

for k in range(N):
    for i in range(n):
        trl.forward(r * dphi)
        trl.right(90)
        trl.forward(dr)
        r += dr
        trl.left(90)
        trl.left(dphi * 360 / 6.28)

input()
