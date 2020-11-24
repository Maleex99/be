# -*- coding: utf-8 -*-
import re
import numpy as np   
from math import inf

from Param import Param

class ParamRobot(Param):
    '''
    Classe permettant de lire et écrire dans un fichier de paramétre du robot.
    '''
    def __init__(self):
        self.param = {}
        self.fileName = "robot_param"
        
        self.load()

    
    def load(self):
        lines = []
        with open(self.fileName, "r") as param_file:
            for line in param_file:
                lines.append(line)
        
        self.param = {}
        path = []
        for line in lines:
            line = re.sub('[\n]', "", line)
            p = re.split("[: ]", line)
            
            thisPath = []
            
            for i,value in enumerate(p.copy()):
                if value != "":
                    thisPath = path[:i]
                    p = p[i:]
                    break
            
            if len(p) < 2:
                continue
            
            path = thisPath
            
            if p[1] == "":
                path.append(p[0])
                continue
            else :
                thisPath.append(p[0])
                thisPath = ":".join(thisPath)
                self.set_param(thisPath, p[1])

        self.param['t34'] = self.load_t34()
        
    def load_t34(self):
        try:
            return np.genfromtxt('t34',delimiter=' ',encoding="utf8")
        except :
            return np.eye(4)

    def save(self):
        save = self.dictToSerial(self.param, 0)
        print(save)
        with open(self.fileName, "w") as param_file:
            param_file.write(save)
        
        t34 = self.get_param("t34")
        with open("t34", "w") as t34_file:
            np.savetxt(t34_file, t34)
        
    def get_posmax(self, *index):
        vmax = []
        for i in index:
            path = "q" + str(i) + ":pos:max"
            vmax.append(self.get_param(path, val_def=inf, type_var=float))
        return vmax
        
    def get_vmax(self, *index):
        vmax = []
        for i in index:
            path = "q" + str(i) + ":vmax"
            vmax.append(self.get_param(path, val_def=inf, type_var=float))
        return vmax
    
    def get_amax(self, *index):
        vmax = []
        for i in index:
            path = "q" + str(i) + ":amax"
            vmax.append(self.get_param(path, val_def=inf, type_var=float))
        return vmax
    
    def get_posmin(self, *index):
        vmax = []
        for i in index:
            path = "q" + str(i) + ":pos:min"
            vmax.append(self.get_param(path, val_def=-inf, type_var=float))
        return vmax