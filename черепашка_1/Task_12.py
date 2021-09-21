import turtle as trl

def draw_spring(R, r, n, Dir=True):
    trl.setheading(90)

    if not Dir:
        R = - R
        r = - r

    for i in range(n-1):
        trl.circle(R, 180)
        trl.circle(r, 180)
    trl.circle(R, 180)
    

trl.speed(0) 
trl.shape('turtle')
trl.setheading(90)

trl.penup()
trl.goto(-200, 0);
trl.pendown()

n = 10

draw_spring(25, 5, n, False)
input()
