# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
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

def plotPoint2D(coord, nom = ""):
    '''
    Fonction pour afficher un point avec un nom sur un graphique 2D
    '''
    plt.scatter(coord[0], coord[1], c = 'Y', marker = 'o')
    plt.annotate(nom, coord)
    
def plotPoint3D(coord, ax, nom = ""):
    '''
    Fonction pour afficher un point avec un nom sur un graphique 3D
    '''
    ax.scatter(coord[0], coord[1], coord[2], c = 'Y', marker = 'o')
    ax.text(coord[0], coord[1], coord[2], nom)