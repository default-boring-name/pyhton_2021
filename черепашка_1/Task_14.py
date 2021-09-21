import turtle as trl
import math

def draw_star_n(x, y, r, n):
    d = (n - 1)/2


    trl.penup();
    trl.goto(x + 0, y + r)
    trl.pendown()

    for i in range(1, n+1):

        phi = 2 * math.pi * i * d / n
        
        trl.goto(x + r * math.sin(phi), y + r * math.cos(phi))
    


trl.speed(0) 
trl.shape('turtle')
trl.setheading(90)


r = 100

draw_star_n(-150, 0, r, 5)
draw_star_n(150, 0, r, 11)




input()
