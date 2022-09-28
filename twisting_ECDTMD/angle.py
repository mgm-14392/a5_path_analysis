import math
import numpy as np
import sys

dot_prod = sys.argv[1:]

angles=[]
for i in dot_prod:
    angle = np.arccos(float(i))
    angles.append(math.degrees(angle))

print(sum(angles)/len(angles))
