import turtle as trl
import time


trl.shape('turtle')
trl.speed(0)
trl.goto(-500,0)
trl.goto(500,0)

fps = 100
dt = 1/fps

T = 20
curr_time = 0

print(dt/50)

scale = 10

q = [0, 0]
v = [2, 20]
a = [0, -10]

print_time = 0
while(curr_time < T):

    trl.goto(scale * q[0] - 400, scale * q[1])

    q = [q[0]+v[0]*dt, q[1]+v[1]*dt]
    v = [v[0]+a[0]*dt, v[1]+a[1]*dt]

    if q[1] <= 0 and v[1] < 0:
        v[1] = -0.8 * v[1]
    
    curr_time += dt
    time.sleep(dt/50)
    
    if curr_time - print_time >= 50 * dt:
        print(round(curr_time, 3))
        print_time = curr_time
        
print('End')
input()
