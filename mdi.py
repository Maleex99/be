# -*- coding: utf-8 -*-

import numpy as np
from math import sin,cos


def MDI(dxp, dphi, qi ,t34):
    '''
    Fonction pour calculer un MDI

    Parameters
    ----------
    dxp : list de float
        Translation sur x, y, z : [dx, dy, dz].
    dphi : list de float
        Rotaion sur x, y, z : [drx, dry, drz].
    qi : list de float
        Postion des qi du robot : [q1, q2, q3].
    t34 : np.array() 4x4
        Matrice homogène t34.

    Raises
    ------
    ValueError
        Erreur lorsque le mouvement demandé n'est pas réalisable par le robot dans cette configuration.

    Returns
    -------
    list de float
        Liste des dqi : [dq1, dq2, dq3].

    '''
    q1, q2, q3 = qi
    
    s1 = sin(q1)
    c1 = cos(q1)
    s3 = sin(q3)
    c3 = cos(q3)
    
    R03 =  np.array([[s1*s3, s1*c3, c1],
                    [-c1*s3, -c1*c3, c1],
                    [c3, -s3, 0]])
    
    P34_3 = t34[:3,3]
    P34_0 = np.dot(R03 ,P34_3)
    
    dp = dxp - np.cross(dphi, P34_0)
    
    dpx, dpy, dpz = dp
    dphix, dphiy, dphiz = dphi
    
    
    
    J = np.array([[-q2, 0, 0],
                  [0  , 1, 0],
                  [0  , 0, 0],
                  [0  , 0, 1],
                  [0  , 0, 0],
                  [1  , 0, 0]])
    
    d = np.array([[c1 * dpx + s1 * dpy],
                  [-s1 * dpx + c1 * dpy],
                  [dpz],
                  [c1 * dphix + s1 * dphiy],
                  [-s1 * dphix + c1 * dphiy],
                  [dphiz]])
    
    Jd = np.hstack((J, d))

    if np.linalg.matrix_rank(Jd) == 3:
        J_inv = np.linalg.pinv(J)
        return np.transpose(np.dot(J_inv, d)).tolist()[0]
    else:
        raise ValueError("Mouvement impossible !")