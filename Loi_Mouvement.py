# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt

def getA(a0, a1, a2, posB,tf):
    ''' Fonction pour obtenir A'''
    return (posB - a0 - a1*tf - a2 * tf**2)/ tf**3

def getB(a1, a2, vitB, tf):
    ''' Fonction pour obtenir B'''
    return (vitB - a1 - 2*a2 * tf) / tf**2

def getC(a2, accB, tf):
    ''' Fonction pour obtenir C'''
    return (accB - 2*a2) / tf

def geta0(posA):
    ''' Fonction pour obtenir a0'''
    return posA

def geta1(vitA):
    ''' Fonction pour obtenir a1'''
    return vitA

def geta2(accA):
    ''' Fonction pour obtenir a2'''
    return accA / 2.0

def geta3(A, B, C):
    ''' Fonction pour obtenir a3'''
    return 10*A - 4*B + C/2.0

def geta4(A, B, C, tf):
    ''' Fonction pour obtenir a4'''
    return (-15*A + 7*B - C) / tf

def geta5(A, B, C, tf):
    ''' Fonction pour obtenir a5'''
    return (12*A - 6*B + C) / (2.0 * tf**2)
    
def getTfQ(posA, vitA, accA, posB, vitB, accB, vMax, aMax, pas = 0.001):
    ''' Fonction pour obtenir Tf optimal à 1ms prés'''
    vMaxCalc = sys.float_info.max
    aMaxCalc = sys.float_info.max

    tf = pas
    a0 = geta0(posA)
    a1 = geta1(vitA)
    a2 = geta2(accA)
    
    while tf < 10**4:   #On ne calcule pas pour un temps Tf supérrieur à 10 000s
        # Obtention des cohéficients de nos équations
        A = getA(a0, a1, a2, posB, tf)
        B = getB(a1, a2, vitB, tf)
        C = getC(a2, accB, tf)
        
        a3 = geta3(A, B, C)
        a4 = geta4(A, B, C, tf)
        a5 = geta5(A, B, C, tf)
    
        # Création des équations nésséssaire pour verifier que aMax(tf) < aMax et vMax(tf) < vMax
        vit = np.poly1d([5*a5, 4*a4, 3*a3, 2*a2, a1])
        acc = np.poly1d([20*a5, 12*a4, 6*a3, 2*a2])
        derv_acc = acc.deriv()
        derv2_acc = acc.deriv(2)
        
        # Récupération de vMax(tf)
        rootAcc = acc.r
        
        rootAcc = rootAcc[rootAcc > 0]
        rootAcc = rootAcc[rootAcc < tf]
        
        xVMax = rootAcc[derv_acc(rootAcc) < 0]
        
        if len(xVMax) == 0:
            xVMax = [vit(0), vit(tf)]
        
        vMaxCalc = max(np.abs(vit(xVMax)))
        
        # Récupération de aMax(tf)
        xAMax = derv_acc.r
        xAMax = xAMax[xAMax > 0]
        xAMax = xAMax[xAMax < tf]
        
        xAMax = xAMax[derv2_acc(xAMax) < 0]
        
        if len(xAMax) == 0:
            xAMax = [acc(0), acc(tf)]
        
        aMaxCalc = max(np.abs(acc(xAMax)))
        
        # Vérification des contrainte de tf (aMax(tf) < aMax et vMax(tf) < vMax) 
        if (vMaxCalc <= vMax) and (aMaxCalc <= aMax):
            return tf
        
        else:
            tf += pas
    
    return None # valeur de tf > 10 000 s




def polyCommande(posA, vitA, accA, posB, vitB, accB, vMax = [10.0, 10.0, 10.0], aMax = [10.0, 10.0, 10.0], te = 0.001):
    ''' Fonction retournant les equations de commande des qi'''
    
    # Le nombre de Qi pour lesquels on doit trouver les equations de commande
    nbQi = len(posA)
    
    tfs = [] # Liste contenant le tf optimal pour chaque qi
    
    # Récupération des tfs optimaux
    for i in range(nbQi):
        tf = getTfQ(posA[i], vitA[i], accA[i], posB[i], vitB[i], accB[i], vMax[i], aMax[i], te)
        if tf is None:
            raise ValueError("tf > 10 000 s")
        tfs.append(tf)
    
    # Conservation du tf maximal pour la sinchronisation des axes
    tf = max(tfs)
    
    # Récupération des coéficiants des équations de commande
    a0 = geta0(np.array(posA))
    a1 = geta1(np.array(vitA))
    a2 = geta2(np.array(accA))
    
    A = getA(a0, a1, a2, np.array(posB), tf)
    B = getB(a1, a2, np.array(vitB), tf)
    C = getC(a2, np.array(accB), tf)
    
    a3 = geta3(A, B, C)
    a4 = geta4(A, B, C, tf)
    a5 = geta5(A, B, C, tf)
    
    pos = []    # liste contenant tout les équation de position pour chaque qi
    vit = []    # liste contenant tout les équation de vitesse pour chaque qi
    acc = []    # liste contenant tout les équation de accélération pour chaque qi
    # Génération des équations de commande pour chaque qi
    for i in range(nbQi):
        pos.append( np.poly1d([a5[i], a4[i], a3[i], a2[i], a1[i], a0[i]]) )
        vit.append( np.poly1d([5*a5[i], 4*a4[i], 3*a3[i], 2*a2[i], a1[i]]) )
        acc.append( np.poly1d([20*a5[i], 12*a4[i], 6*a3[i], 2*a2[i]]) )
    
    return (pos, vit, acc, tf)




if __name__ == "__main__":
                                    #   qA       qA.      qA..     qB       qB.      qB..
   (pos, vit, acc, tf) = polyCommande([0,0,0], [0,0,0], [0,0,0], [1,2,3], [1,1,7], [0,0,0])
   
   x = np.arange(0, tf, 0.001)
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