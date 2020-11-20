# -*- coding: utf-8 -*-

import numpy as np   
    
def inverse_mat_homogene(m):
    '''
    Fonction pour inverser une matrice de passage
    '''
    R = np.transpose(m[:3,:3])
    P = -np.dot(R, m[:3,3])
    return np.insert(np.c_[R,P], 3,[0, 0, 0, 1], axis=0)

def extract_xyz(m):
    '''
    Fonction pour récupérer P d'une matrice de passage
    '''
    return tuple(m[:3,3])