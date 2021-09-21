import turtle as trl

def draw_0(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x+d, y-2*d)
    trl.goto(x, y-2*d)
    trl.goto(x, y)

def draw_1(x, y, d):
    trl.penup()
    trl.goto(x, y-d)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x+d, y-2*d)

def draw_2(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x+d, y-d)
    trl.goto(x, y-2*d)
    trl.goto(x+d, y-2*d)

def draw_3(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x, y-d)
    trl.goto(x+d, y*d)
    trl.goto(x, y-2*d)

def draw_4(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x, y-d)
    trl.goto(x+d, y-d)
    trl.goto(x+d, y)
    trl.goto(x+d, y-2*d)

def draw_5(x, y, d):
    trl.penup()
    trl.goto(x+d, y)

    trl.pendown()
    trl.goto(x, y)
    trl.goto(x, y-d)
    trl.goto(x+d, y-d)
    trl.goto(x+d, y-2*d)
    trl.goto(x, y-2*d)

def draw_6(x, y, d):
    trl.penup()
    trl.goto(x+d, y)

    trl.pendown()
    trl.goto(x, y-d)
    trl.goto(x, y-2*d)
    trl.goto(x+d, y-2*d)
    trl.goto(x+d, y-d)
    trl.goto(x, y-d)

def draw_7(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x, y-d)
    trl.goto(x, y-2*d)

def draw_8(x, y, d):
    trl.penup()
    trl.goto(x, y)

    trl.pendown()
    trl.goto(x+d, y)
    trl.goto(x+d, y-2*d)
    trl.goto(x, y-2*d)
    trl.goto(x, y)
    trl.goto(x, y-d)
    trl.goto(x+d, y-d)

def draw_9(x, y, d):
    trl.penup()
    trl.goto(x, y-2*d)

    trl.pendown()
    trl.goto(x+d, y-d)
    trl.goto(x+d, y)
    trl.goto(x, y)
    trl.goto(x, y-d)
    trl.goto(x+d, y-d)

def draw_n(n, x, y, d, mrg, f):
    draw = (draw_0,
        draw_1,
        draw_2,
        draw_3,
        draw_4,
        draw_5,
        draw_6,
        draw_7,
        draw_8,
        draw_9)
    
    normal_width = trl.width()
    trl.width(f)
    
    stack = map(int, list(str(n)))
    x_i = x
    
    for i in stack:
        draw[i](x_i, y, d)
        x_i += d + mrg
        
    trl.width(normal_width)
        


trl.shape('turtle')
trl.speed(5)

draw_n(141700, x=-100, y=100, d=20, mrg=5,  f=3)

input()
