import numpy as np

def qi_MGI(l_xyz, m, t34, epsilon3=-1, epsilon1=1):
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