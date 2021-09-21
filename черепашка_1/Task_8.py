import turtle as trl

trl.speed(0)
 
trl.shape('turtle')
N = 20
dl = 5;
l = dl;

trl.penup()
trl.goto(l, 0)
trl.setheading(90)
trl.pendown()

for k in range(N):
    for i in range(4):
        trl.forward(l)
        trl.left(90)
        l += dl;

input()
