import turtle as trl

trl.speed(0) 
trl.shape('turtle')
trl.setheading(90)

R = 100
r = 20
r_s = 50

trl.penup()
trl.goto(R, 0)
trl.pendown()

trl.color('yellow')
trl.begin_fill()
trl.circle(R)
trl.end_fill()
trl.color('black')
trl.circle(R)


trl.penup()
trl.goto(-R * 0.4 + r, R * 0.4)
trl.pendown()


trl.color('blue')
trl.begin_fill()
trl.circle(r)
trl.end_fill()
trl.color('black')
trl.circle(r)


trl.penup()
trl.goto(R * 0.4 + r, R * 0.4)
trl.pendown()


trl.color('blue')
trl.begin_fill()
trl.circle(r)
trl.end_fill()
trl.color('black')
trl.circle(r)


trl.penup()
trl.goto(0, R * 0.2)
trl.pendown()

trl.width(8)
trl.goto(0, -R * 0.2)
trl.width(1)


trl.penup()
trl.goto(r_s, -R * 0.3)
trl.pendown()

trl.left(180)
trl.width(8)
trl.color('red')
trl.circle(-r_s, 180)
trl.width(1)
trl.color('black')

input()
