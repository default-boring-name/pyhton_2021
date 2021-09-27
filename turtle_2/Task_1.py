import turtle as trl
import random
import math

trl.shape('turtle')
trl.speed(2)


N = 1000
r= 10
coors = [0, 0]

for i in range(N):
    phi = random.random() * 2 * math.pi
    coors[0] += r * math.cos(phi)
    coors[1] += r * math.sin(phi)
    print(coors)
    trl.goto(*coors)

input()
