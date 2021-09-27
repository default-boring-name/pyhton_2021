import turtle as trl
import time
import random
import math


borders = (200, 200)
fps = 100
dt = 1/fps
max_time = 10

class molecule:
    def __init__(self, q, v):
        
        self.trl = trl.Turtle(shape='circle')
        self.trl.shapesize(stretch_wid = 0.5, stretch_len = 0.5)
        self.trl.speed(0)
        self.trl.penup()
        self.trl.goto(q[0], q[1])
        
        self.q = list(q)
        self.v = list(v)
    def animate(self):
        self.q = [self.q[0]+self.v[0]*dt, self.q[1]+self.v[1]*dt]
        
        if (self.q[0] < -borders[0] and self.v[0] < 0
            or self.q[0] > borders[0] and self.v[0] > 0):
            self.v[0] = -self.v[0]
            
        if (self.q[1] < -borders[1] and self.v[1] < 0
            or self.q[1] > borders[1] and self.v[1] > 0):
            self.v[1] = -self.v[1]
            
def draw_line(start, end):
    trl.penup()
    trl.goto(*start)
    trl.pendown()
    trl.goto(*end)

curr_time = 0

offset = (0,0)


trl.shape('circle')
trl.shapesize(stretch_wid = 0.5, stretch_len = 0.5)
trl.speed(0)

draw_line((borders[0]*-1, borders[1]*-1),
          (borders[0]*-1, borders[1]*+1))
draw_line((borders[0]*+1, borders[1]*-1),
          (borders[0]*+1, borders[1]*+1))
draw_line((borders[0]*-1, borders[1]*-1),
          (borders[0]*+1, borders[1]*-1))
draw_line((borders[0]*-1, borders[1]*+1),
          (borders[0]*+1, borders[1]*+1))

obj_number = 50
objs = []

for i in range(obj_number):
    
    q = [100 * (random.random() - 0.5), 100 * (random.random() - 0.5)]
    
    phi = 2 * math.pi * random.random()
    v = [200 * math.cos(phi), 200 * math.sin(phi)]
    
    objs.append(molecule(q, v))
    


while(curr_time < max_time):

    for obj in objs:
        obj.trl.goto(obj.q[0], obj.q[1])
        obj.animate()

    
    curr_time += dt
    time.sleep(dt)
    
        
print('End')
input()
