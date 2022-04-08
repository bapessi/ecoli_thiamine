import numpy as np
import pandas as pd
from scipy import integrate

def ODE():
    v_glc = 1
    v_lac = 2
    v_b = 1
    dGLCdt = -v_glc
    dLACdt = v_lac
    dPYRdt =  v_glc -v_b -v_lac
    dBdt = v_b
    v_array = np.array([v_glc,v_lac,v_b]) 

    K = np.array([  [1,2,3],
                    [4,5,6],
                    [-2,-2,-2],
                    [2,2,2]
                ])
    print(K)
    print(v_array)
    dMdt = np.matmul(K,v_array)
    return dMdt

dMdt = ODE()
print(dMdt)
