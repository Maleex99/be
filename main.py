# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np

import util as u

from ParamPoints import ParamPoints
from ParamRobot import ParamRobot

from mgi import MGI_opti as MGI
from mdi import MDI
from mgd import MGD
from mdd import MDD

from Loi_Mouvement import getPolyCommande

def display_point(param_points, values, tf, te):
    '''Fonction pour afficher des points sur une courbe 2D à un t donnée.'''
    u.plotPoint2D((0, values[0]), param_points.get_nom(0))
    
    tfin = 0
    for i,t in enumerate(tf):
        tfin += t
        u.plotPoint2D((tfin, values[int(tfin/te)-1]), param_points.get_nom(i+1))

def display_qi(ypos, yvit, yacc, tf, te, param_points):
    '''Fonction pour afficher les courbes des qi.'''
    for i in range(3):
        x = np.arange(0, np.sum(tf)-te, te)
        
        plt.figure(i)
            
        plt.subplot(3,1,1)
        plt.title("q"+str(i+1))
        plt.xticks([])
        plt.ylabel("Position")
        plt.plot(x, ypos[i])
        display_point(param_points, ypos[i], tf, te)
        
        plt.subplot(3,1,2)
        plt.xticks([])
        plt.ylabel("Vitesse")
        plt.plot(x, yvit[i])
        display_point(param_points, yvit[i], tf, te)
        
        plt.subplot(3,1,3)
        plt.ylabel("Acélération")
        plt.plot(x, yacc[i])
        display_point(param_points, yacc[i], tf, te)
        
        plt.xlabel("Time (s)")
    
    plt.show()
    
def display_traj(pos, param_points, param_robot):
    '''Fonction pour afficher la courbe de la trajectoir du robot en 3D à l'aide du MGD.'''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    for i in range(param_points.get_nbPoints()):
        u.plotPoint3D(param_points.get_pos(i), ax, param_points.get_nom(i))
    
    p = np.transpose(np.array(pos))
    
    m = param_robot.get_param("m")
    t34 = param_robot.get_param("t34")
    
    xyz = []
    for q in p:
        q1, q2, q3 = q;
        
        t03 = MGD((q1, q2, q3), m)
        t04 = np.dot(t03, t34)
        
        coord = list(u.extract_xyz(t04))
        xyz.append(coord)
        
    xyz = np.round(xyz, 3)
    
    xyz = np.array(xyz)
    
    ax.plot(xyz[:,0], xyz[:,1], xyz[:,2])
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()


def display_vit_xyz(qi, dqi, param_points, param_robot, tf, te):
    '''Fonction pour afficher les vitesse sur les axe x, y et z à l'aide du MDD'''
    t34 = param_robot.get_param("t34")
    
    dxt = []
    dphit = []
    
    qi = np.transpose(np.array(qi))
    dqi = np.transpose(np.array(dqi))
    
    for i,q in enumerate(qi):
        dq = dqi[i]
        dx, dphi = MDD(q, dq, t34)
        dxt.append(dx)
        dphit.append(dphi)
        
    plt.figure()
    
    title = ["dx", "dy", "dz"]
    title1 = ["dphix", "dphiy", "dphiz"]
    
    x = np.arange(0, np.sum(tf)-te, te)
    
    dxt = np.round(np.array(dxt), 3)
    dphit = np.round(np.array(dphit), 3)
    
    for i in range(3):
        plt.subplot(3,2,1+i*2)
        if i == 2:
            plt.xlabel("Time (s)")
        else :
            plt.xticks([])
        plt.title(title[i])
        plt.plot(x, dxt[:,i])
        display_point(param_points, dxt[:,i], tf, te)
        
        plt.subplot(3,2,2+i*2)
        if i == 2:
            plt.xlabel("Time (s)")
        else :
            plt.xticks([])
        plt.title(title1[i])
        plt.plot(x, dphit[:,i])
        display_point(param_points, dphit[:,i], tf, te)
        
    plt.show()

def display(pos, vit, acc, tf, te, param_points, param_robot):
    '''Fonction pour afficher tous les graphiques des valeurs du robot.'''
    pos_t = [[],[],[]]
    vit_t = [[],[],[]]
    acc_t = [[],[],[]]
    
    for i in range(3):
        for j in range(len(pos)):
            tfin = tf[j]
            x = np.arange(0+te, tfin, te)
            
            pos_t[i] += pos[j][i](x).tolist()
            vit_t[i] += vit[j][i](x).tolist()
            acc_t[i] += acc[j][i](x).tolist()
            
    display_qi(pos_t, vit_t, acc_t, tf, te, param_points)
    
    display_traj(pos_t, param_points, param_robot)
    
    display_vit_xyz(pos_t, vit_t, param_points, param_robot, tf, te)
        
        

if __name__ == "__main__":
    
    param_points = ParamPoints("position")
    params = ParamRobot()
    
    nb_points = param_points.get_nbPoints();
    
    t34 = params.get_param('t34', np.eye(4))
    t43 = u.inverse_mat_homogene(t34)
    m = params.get_param('m', 2, float)
    qi_prev = [0, 0, 0]
    
    qi_min = params.get_posmin(1,2,3)
    qi_max = params.get_posmax(1,2,3)
    
    # calcul la valeur des qi et des dqi pour chaque points
    point_qi = []
    point_dqi = []
    for i in range(nb_points):
        xyz = param_points.get_pos(i)
        
        qi = []
        try:
            qi = MGI(xyz, m, t34, qi_min=qi_min, qi_max=qi_max, qi_prev=qi_prev)
            point_qi.append(qi)
            qi_prev = qi
        
        except ValueError:
            print("La postion du point " + param_points.get_nom(i) + " est impossible !")
            sys.exit()
        
        
        dx, dphi = param_points.get_vit(i)
        
        dqi = []
        try:
            dqi = MDI(dx, dphi, qi, t34)
            point_dqi.append(dqi)
        
        except ValueError:
            print("Le movement au point " + param_points.get_nom(i) + " est impossible !")
            sys.exit()
    
    vMax = params.get_vmax(1,2,3)
    aMax = params.get_amax(1,2,3)
    te = params.get_param("Te", 0.001, float)
    
    pos = []
    vit = []
    acc = []
    tf = []
    for i in range(1, nb_points):
        (p, v, a, t) = getPolyCommande(point_qi[i-1], point_dqi[i-1], [0,0,0], point_qi[i], point_dqi[i], [0,0,0], vMax=vMax, aMax=aMax, te=te)
        pos.append(p)
        vit.append(v)
        acc.append(a)
        tf.append(t)
        
    display(pos, vit, acc, tf, te, param_points, params)
        