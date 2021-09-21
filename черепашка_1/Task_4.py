import turtle as trl

trl.speed(0)
 
trl.shape('turtle')

trl.penup()

trl.goto(50,0)
trl.left(90)

trl.pendown()

n = 30
r = 50

for i in range(n):
    trl.forward(r * 2 * 3.14 / n);
    trl.left(360.0 / n);

input()
