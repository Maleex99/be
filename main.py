# -*- coding: utf-8 -*-

from mgd import MGD as MGD
from mgi import MGI_opti as MGI
from Loi_Mouvement import getPolyCommande
from ParamRobot import ParamRobot
import util as u
import numpy as np
import matplotlib.pyplot as plt

def display_qi_command(pos, vit, acc, tf, te):
   x = np.arange(0, tf, te)
   for i in range(3):
       ypos = pos[i](x)
       yvit = vit[i](x)
       yacc = acc[i](x)
       
       plt.figure(i)
       
       plt.subplot(3,1,1)
       plt.title("q"+str(i+1))
       plt.xticks([])
       plt.ylabel("Position")
       plt.plot(x, ypos)
       
       plt.subplot(3,1,2)
       plt.xticks([])
       plt.ylabel("Vitesse")
       plt.plot(x, yvit)
       
       plt.subplot(3,1,3)
       plt.ylabel("Acélération")
       plt.plot(x, yacc)
       
       plt.xlabel("Time (s)")
       
       plt.show()
       
def display_3D_mouvement(points, depart, arrive):
    points = np.array(points)
    
    depart = np.round(depart, 2)
    arrive = np.round(arrive, 2)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(points[:,1], points[:,0], points[:,2])
    ax.scatter(depart[1],depart[0],depart[2], c = 'g', marker = 'o')
    ax.scatter(arrive[1],arrive[0],arrive[2], c = 'r', marker = 'o')
    
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')
    
    plt.show()


if __name__ == "__main__":

    n = 2 # nombre de points
    
    params = ParamRobot()
    
    points_xyz = [[] for i in range(n)]
    point_qi = []
    t34 = params.get_param('t34', np.eye(4))
    t43 = u.inverse_mat_homogene(t34)
    m = params.get_param('m', 2, float)
    qi_prev = [0, 0, 0]
    
    # Récupération des coordonnées x, y ,z de n points
    qi_min = params.get_posmin(1,2,3)
    qi_max = params.get_posmax(1,2,3)
    for i,point in enumerate(points_xyz):
        for axe in ("x", "y", "z"):
            coord = None
            while coord is None:
                coord = input("Quel est le " + axe + " pour le point " + str(i) + " ?\n")
                try:
                    coord = float(coord)
                    point.append(coord)
                    pass
                except ValueError:
                    print("Erreur : " + axe + " doit être un nombre décimal !\n")
                    coord = None
                    pass
        qi_prev = MGI(point, m, t34, qi_min=qi_min, qi_max=qi_max, qi_prev=qi_prev)
        point_qi.append( qi_prev )
    
    
    vMax = params.get_vmax(1,2,3)
    aMax = params.get_amax(1,2,3)
    te = params.get_param("Te", 0.001, float)
    (pos, vit, acc, tf) = getPolyCommande(point_qi[0], [0,0,0], [0,0,0], point_qi[1], [0,0,0], [0,0,0], vMax=vMax, aMax=aMax, te=te)
    
    display_qi_command(pos, vit, acc, tf, te)
    
    pos_t = []
    for t in np.arange(0, tf, te):
        q1 = pos[0](t)
        q2 = pos[1](t)
        q3 = pos[2](t)
        
        t03 = MGD((q1, q2, q3), m)
        t04 = np.dot(t03, t34)
        
        coord = list(u.extract_xyz(t04))
        
        pos_t.append(coord)
    
    display_3D_mouvement(pos_t, points_xyz[0], points_xyz[1])