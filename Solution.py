import matplotlib.pyplot as plt
import math
import random
import numpy as np
import global_var as gl

def is_valid(X,Y, mmp):
    n = len(X)
    if len(Y) != n:
        return False
    for i in range(n):
        x,y = X[i],Y[i]
        if x < 0 or x >= gl.col or y < 0 or y >= gl.row:
           return False
        #if mmp[y][x] == 0:
        #    return False
    for i in range(n):
        ok = False
        for j in range(n):
            if i == j:
                continue
            dis = (X[i]-X[j])**2
            dis += (Y[i] - Y[j])**2
            dis = math.sqrt(dis)
            if dis <= gl.max_flight_radius:
                ok = True
        if ok == False:
            return False
    return True