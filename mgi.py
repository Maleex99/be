import numpy as np
from math import atan2, sqrt, inf

def qi_MGI(l_xyz, m, t34, epsilon3=-1, epsilon1=1): # MARCHE PO
    result = []
    # q3
    denum = t34[0][3]**2 + t34[1][3]**2
    if denum == 0:
        q3 = 0
        s3 = np.sin(q3)
        c3 = np.cos(q3)
    else:
        num = (-1)*t34[1][3]*(l_xyz[2]-m)+epsilon3*t34[0][3]*np.sqrt(t34[0][3]**2+t34[1][3]**2-(l_xyz[2]-m)*(l_xyz[2]-m))
        s3 = num/denum
        num = t34[0][3]*(l_xyz[2]-m)+epsilon3*t34[1][3]*np.sqrt(t34[0][3]**2+t34[1][3]**2-(l_xyz[2]-m)*(l_xyz[2]-m))
        c3 = num/denum
        q3 = np.arctan2(s3, c3)
    # q1
    denum = l_xyz[0]**2+l_xyz[1]**2
    if denum == 0:
        q1 = 0
        s1 = np.sin(q1)
        c1 = np.cos(q1)
    else:
        num = l_xyz[1]*t34[2][3]+epsilon1*l_xyz[0]*np.sqrt(l_xyz[0]**2+l_xyz[1]**2-t34[2][3]**2)
        s1 = num/denum
        num = l_xyz[0]*t34[2][3]+epsilon1*l_xyz[1]*np.sqrt(l_xyz[0]**2+l_xyz[1]**2-t34[2][3]**2)
        c1 = num/denum
        q1 = np.arctan2(s1, c1)
    # q2
    q2 = s3*t34[0][3]+c3*t34[1][3]-s1*l_xyz[0]+c1*l_xyz[1]
    # fill result
    result.append(q1)
    result.append(q2)
    result.append(q3)
    return result

def get_qi(a, B, g, E):
    si = (B * g + E * a * sqrt(a**2 + B**2 - g**2) ) / (a**2 + B**2)
    ci = (a * g - E * B * sqrt(a**2 + B**2 - g**2) ) / (a**2 + B**2)
    qi = atan2(si, ci)
    return (si, ci, qi)

def test_qi(qi, qi_min, qi_max, i):
    if qi > qi_max:
        raise ValueError("q" + i + " > q" + i + " max")
    elif qi < qi_min:
        raise ValueError("q" + i + " < q" + i + " min")

def MGI(xyz, m, t34, E1 = -1, E3 = 1, qi_min = [-inf, -inf, -inf], qi_max = [inf, inf, inf]):
    x,y,z = xyz
    
    t34x = t34[0,3]
    t34y = t34[1,3]
    t34z = t34[2,3]
    
    # q1
    
    q1 = 0
    s1 = 0
    c1 = 0
    
    if x == 0 and y == 0 and t34z == 0:
        c1 = 1
    elif  x**2 + y**2 >= t34z**2:
        s1, c1, q1 = get_qi(x, y, t34z, E1)
    else:
        raise ValueError("Position impossible !")
    
    test_qi(q1, qi_min[0], qi_max[0], 1)
    
    # q3

    q3 = 0
    s3 = 0
    c3 = 0
    
    if t34x == 0 and -t34y == 0 and z-m == 0:
        c3 = 1
    elif t34x**2 + t34y**2 >= (z-m)**2:
        s3, c3, q3 = get_qi(t34x, -t34y, z-m, E3)
    else:
        raise ValueError("Position impossible !")
        
    test_qi(q3, qi_min[2], qi_max[2], 3)
        
    
    # q2
    q2 = y * c1 - x * s1 + s3 * t34x + c3 * t34y
    
    test_qi(q2, qi_min[1], qi_max[1], 2)
    
    return (q1, q2, q3)

def MGI_opti(xyz, m, t34, qi_min = [-inf, -inf, -inf], qi_max = [inf, inf, inf], qi_prev = [0, 0, 0]):
    qis = []
    qi_distance = []
    for E1 in (-1, 1):
        for E3 in (-1, 1):
            try:
                qi = MGI(xyz, m, t34, E1=E1, E3=E3, qi_min=qi_min, qi_max=qi_max)
                distance = np.linalg.norm( np.subtract(qi, qi_prev) )
                
                qis.append(qi)
                qi_distance.append(distance)
            except ValueError:
                continue
    
    if len(qis) == 0:
        raise ValueError("Position impossible !")
    
    opti_index = np.argmin(qi_distance)
    return qis[opti_index]