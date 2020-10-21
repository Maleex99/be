# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt

def getA(a0, a1, a2, posB,tf):
    return (posB - a0 - a1*tf - a2 * tf**2)/ tf**3

def getB(a1, a2, vitB, tf):
    return (vitB - a1 - 2*a2 * tf) / tf**2

def getC(a2, accB, tf):
    return (accB - 2*a2) / tf

def geta0(posA):
    return posA

def geta1(vitA):
    return vitA

def geta2(accA):
    return accA / 2.0

def geta3(A, B, C):
    return 10*A - 4*B + C/2.0

def geta4(A, B, C, tf):
    return (-15*A + 7*B - C) / tf

def geta5(A, B, C, tf):
    return (12*A - 6*B + C) / (2.0 * tf**2)
    
def getTfQ(posA, vitA, accA, posB, vitB, accB, vMax, aMax):
    vMaxCalc = sys.float_info.max
    aMaxCalc = sys.float_info.max
    
    pas = 1

    tf = pas
    a0 = geta0(posA)
    a1 = geta1(vitA)
    a2 = geta2(accA)
    
    i = 0
    
    while i < 10**4:
        A = getA(a0, a1, a2, posB, tf)
        B = getB(a1, a2, vitB, tf)
        C = getC(a2, accB, tf)
        
        a3 = geta3(A, B, C)
        a4 = geta4(A, B, C, tf)
        a5 = geta5(A, B, C, tf)
    
        vit = np.poly1d([5*a5, 4*a4, 3*a3, 2*a2, a1])
        acc = np.poly1d([20*a5, 12*a4, 6*a3, 2*a2])
        derv_acc = acc.deriv()
        derv2_acc = acc.deriv(2)
        
        rootAcc = acc.r
        
        rootAcc = rootAcc[rootAcc > 0]
        rootAcc = rootAcc[rootAcc < tf]
        
        xVMax = rootAcc[derv_acc(rootAcc) < 0]
        
        if len(xVMax) == 0:
            xVMax = [vit(0), vit(tf)]
        
        vMaxCalc = max(np.abs(vit(xVMax)))
        
        xAMax = derv_acc.r
        xAMax = xAMax[xAMax > 0]
        xAMax = xAMax[xAMax < tf]
        
        xAMax = xAMax[derv2_acc(xAMax) < 0]
        
        if len(xAMax) == 0:
            xAMax = [acc(0), acc(tf)]
        
        aMaxCalc = max(np.abs(acc(xAMax)))
        
        if (vMaxCalc <= vMax) and (aMaxCalc <= aMax):
            return tf
        
        else:
            i += 1
            tf += pas
    
    return None




def polyCommande(posA, vitA, accA, posB, vitB, accB, vMax = [10.0, 10.0, 10.0], aMax = [10.0, 10.0, 10.0]):
    
    nbQi = len(posA)
    
    tfs = []
    
    for i in range(nbQi):
        tf = getTfQ(posA[i], vitA[i], accA[i], posB[i], vitB[i], accB[i], vMax[i], aMax[i])
        if tf is None:
            raise ValueError("tf > 10000")
        tfs.append(tf)
    
    tf = max(tfs)
    
    a0 = geta0(np.array(posA))
    a1 = geta1(np.array(vitA))
    a2 = geta2(np.array(accA))
    
    A = getA(a0, a1, a2, np.array(posB), tf)
    B = getB(a1, a2, np.array(vitB), tf)
    C = getC(a2, np.array(accB), tf)
    
    a3 = geta3(A, B, C)
    a4 = geta4(A, B, C, tf)
    a5 = geta5(A, B, C, tf)
    
    pos = []
    acc = []
    vit = []
    for i in range(nbQi):
        pos.append( np.poly1d([a5[i], a4[i], a3[i], a2[i], a1[i], a0[i]]) )
        acc.append( np.poly1d([5*a5[i], 4*a4[i], 3*a3[i], 2*a2[i], a1[i]]) )
        vit.append( np.poly1d([20*a5[i], 12*a4[i], 6*a3[i], 2*a2[i]]) )
    
    return (pos, vit, acc, tf)




if __name__ == "__main__":
                                    #   qA       qA.      qA..     qB       qB.      qB..
   (pos, acc, vit, tf) = polyCommande([0,0,0], [0,0,0], [0,0,0], [1,2,3], [1,1,1], [0,0,0])
   
   x = np.arange(0, tf, 0.01)
   for i in range(3):
       ypos = pos[i](x)
       yvit = vit[i](x)
       yacc = acc[i](x)
       
       plt.figure(i)
       plt.subplot(3,1,1)
       plt.plot(x, ypos)
       
       plt.subplot(3,1,2)
       plt.plot(x, yvit)
       
       plt.subplot(3,1,3)
       plt.plot(x, yacc)