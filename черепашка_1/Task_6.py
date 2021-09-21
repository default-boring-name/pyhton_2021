import turtle as trl

trl.speed(0)
 
trl.shape('turtle')
n = 20
r = 100
for i in range(n):
    trl.right(360.0 / n)
    trl.forward(r)
    trl.stamp()
    trl.backward(r)

input()
