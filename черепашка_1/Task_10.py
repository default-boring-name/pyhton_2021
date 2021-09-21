import turtle as trl


trl.speed(0) 
trl.shape('turtle')

r = 50

for i in range(3):
    trl.circle(r)
    trl.circle(-r)
    trl.left(60)
input()
