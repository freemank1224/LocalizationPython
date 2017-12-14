# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Modify the move function to accommodate the added 
#probabilities of overshooting or undershooting 
#the intended destination.


world=[['green', 'green', 'green', 'green', 'green'],
       ['green', 'red', 'green', 'green', 'green'],
       ['green', 'green', 'red', 'green', 'green'],
       ['green', 'red', 'red', 'green', 'green']]
measurements = ['red', 'green']
pHit = 1.0
pMiss = 0.0
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def initialize(world):
    p_init = 1/(len(world) * len(world[0]))
    p = [[p_init for i in world[0]] for j in world]
    return p
# Single measurement Sensing
def sense(p, world, measurement):
    q=p
    s=0
    for i in range(len(p)):
        for j in range(len(p[0])):
            hit = (measurement == world[i][j])
            q[i][j] = (p[i][j] * (hit * pHit + (1-hit) * pMiss))
            s = s + q[i][j]
#            print(s)
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] = q[i][j] / s
    return q


p = initialize(world)

#p = sense(p,world, 'red')
#p = sense(p,world, 'red')
p = sense(p,world, 'green')
#p = sense(p,world, 'red')
#for measurement in measurements:
#    print(measurement)
#    p = sense(p, world, measurement)




#def move(p, U):
#    qExact = []
#    qOver = []
#    qUnder = []
#    for i in range(len(p)):
#        qExact.append(p[(i-U)%len(p)] * pExact)
#        qOver.append(p[(i-U-1)%len(p)] * pOvershoot)
#        qUnder.append(p[(i-U+1)%len(p)] * pUndershoot)
#        
#    q = list(map(lambda x: x[0]+x[1]+x[2], zip(qExact,qOver,qUnder)))
#    
#    return q
#    
#for k in range(10):
#    p = move(p,1)
    
print(p)