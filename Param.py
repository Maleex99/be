# -*- coding: utf-8 -*-

import re
from math import pi

class Param:
    '''
    Classe permettant de lire et écrire dans un fichier de paramétre.
    '''
    def __init__(self, fileName):
        self.param = {}
        self.fileName = fileName
        self.load()
        
        
    def set_param(self, path, value):
        d = self.param
        p = path.split(":")
        for noeud in p[:-1]:
            if noeud not in d:
                d[noeud] = {}
            d = d[noeud]
        d[p[-1]] = value
        
        
    
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

    def save(self):
        save = self.dictToSerial(self.param, 0)
        print(save)
        with open(self.fileName, "w") as param_file:
            param_file.write(save)
    
    
    def dictToSerial(self, d, rank=0):
        res = ""
        for value in d:
            for i in range(rank):
                    res += " "
                    
            if value == "t34":
                continue
            if type(d[value]) == dict:
                res += str(value) + ":\n"
                res += self.dictToSerial(d[value], rank+1)
            else:
                res += str(value) + ":" + str(d[value]) + "\n"
                
        return res

    def get_param(self, path, val_def = None, type_var = None):
        p = path.split(":")
        d = self.param
        for noeud in p[:-1]:
            if noeud not in d:
                return val_def
            d = d[noeud]      
        
        if p[-1] not in d:
            return val_def
        
        if (type_var is None) or (d[p[-1]] is None):
            return d[p[-1]]
        
        else:
            return type_var( d[p[-1]] )
