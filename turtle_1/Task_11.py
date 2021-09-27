import turtle as trl


trl.speed(0) 
trl.shape('turtle')
trl.setheading(90)

r = 50
n = 15
dr = 8

for i in range(n):
    trl.circle(r)
    trl.circle(-r)
    r += dr
input()
