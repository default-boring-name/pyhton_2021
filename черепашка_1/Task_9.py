import turtle as trl
import math


def draw_n(x, y, r, n):
    trl.penup()
    trl.goto(x + r, y)
    trl.setheading(90)
    trl.pendown()

    alpha = 180 * (n - 2) / n
    phi_rad = 2 * math.pi / n
    d = math.sin(phi_rad / 2) * 2 * r


    trl.left(90 - alpha / 2)
    trl.forward(d)
    
    for i in range(n-1):
        trl.left(180 - alpha)
        trl.forward(d)

trl.speed(0)
 
trl.shape('turtle')
N = 10
r = 50
dr = 30


for k in range(3, 3+N):
    draw_n(0, 0, r, k)
    r += dr

input()
