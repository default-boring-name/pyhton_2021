import turtle as trl

def draw_square(x, y, a):
    trl.penup()
    trl.goto(x + a / 2.0, y)
    trl.setheading(90)
    trl.pendown()

    trl.forward(a / 2.0)

    for i in range(3):
        trl.left(90)
        trl.forward(a)
    
    trl.left(90)
    trl.forward(a / 2.0)
    
trl.speed(0)                
 
trl.shape('turtle')

for a in range(10, 100 + 10, 10):
    draw_square(0, 0, a)


input()
