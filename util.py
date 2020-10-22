# -*- coding: utf-8 -*-

import re
import numpy as np

def load_param():
    param = {}
    lines = ""
    with open("robot_param", "r") as param_file:
        lines = param_file.readlines()
    
    for line in lines:
        line = re.sub('[ \n]', "", line)
        p = re.split("[:]", line)
        try:
            param[p[0]] = float(p[1])
        except IndexError:
            param[p[0]] = None
    
    param['t34'] = get_t34()
    
    return param
    

def get_t34():
    try:
        return np.genfromtxt('t34',delimiter=' ',encoding="utf8")
    except :
        return np.eye(4)
    
def get_t43(t34):
    R = np.transpose(t34[:3,:3])
    P = -np.dot(R, t34[:3,3])
    return np.insert(np.c_[R,P], 3,[0, 0, 0, 1], axis=0)
    
def get_t04(t03, t34 = get_t34()):
    return np.matmul(t03, t34)

def extract_xyz(t):
    return (t[0][3], t[1][3], t[2][3])