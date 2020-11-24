# -*- coding: utf-8 -*-

from Param import Param

class ParamPoints(Param):
    '''
    Classe permettant de lire et écrire dans un fichier contenant les points.
    '''    
    def __init__(self, filename):
        Param.__init__(self, filename)
        
    
    def get_nom(self, index):
        return list(self.param.keys())[index]
    
    def get_nbPoints(self):
        return len(self.param)
    
    def get_pos(self, index):
        keys = list(self.param.keys())
        
        point_name = ""
        try:
            point_name = keys[index]
        except IndexError:
            raise IndexError("list index out of range")
            
        x = self.get_param(point_name + ":pos:x", 0, float)
        y = self.get_param(point_name + ":pos:y", 0, float)
        z = self.get_param(point_name + ":pos:z", 0, float)
        return (x, y, z)
    
    def get_vit(self, index):
        keys = list(self.param.keys())
        
        point_name = ""
        try:
            point_name = keys[index]
        except IndexError:
            raise IndexError("list index out of range")
            
        x = self.get_param(point_name + ":vit:x", 0, float)
        y = self.get_param(point_name + ":vit:y", 0, float)
        z = self.get_param(point_name + ":vit:z", 0, float)
        
        rx = self.get_param(point_name + ":vit:rx", 0, float)
        ry = self.get_param(point_name + ":vit:ry", 0, float)
        rz = self.get_param(point_name + ":vit:rz", 0, float)
        
        return (x, y ,z), (rx, ry, rz)