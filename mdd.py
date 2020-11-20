# -*- coding: utf-8 -*-

import numpy as np
from math import cos, sin

def MDD(pos_q, vit_q, t34):
    q1 , q2, q3 = pos_q
    vq1, vq2, vq3 = vit_q
    t34x, t34y, t34z = t34[:3, 3]
    
    c1 = cos(q1)
    s1 = sin(q1)
    s3 = sin(q3)
    c3 = cos(q3)
    
    dp = np.array([-q2 * vq1 - s1 * vq2,
                   -q2 * vq1 * s1 + c1 * vq2,
                   0])
    
    dphi = np.array([vq3 * c1,
                     vq3 * s1,
                     vq1])
    
    R03 =  np.array([[s1*s3, s1*c3, c1],
                    [-c1*s3, -c1*c3, c1],
                    [c3, -s3, 0]])
    
    P34_3 = t34[:3,3]
    P34_0 = np.dot(R03 ,P34_3)
    
    dxp = dp + np.cross(dphi, P34_0)
    
    return (dxp, dphi)