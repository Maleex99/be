import numpy as np
from math import atan2, sqrt, inf, sin, cos

def get_qi(a, B, g, E):
    '''
    Fonction qui calcule les qi des équation de la forme : a*cos(q) + B*sin(q) = g
    '''
    si = (B * g + E * a * sqrt(a**2 + B**2 - g**2) ) / (a**2 + B**2)
    ci = (a * g - E * B * sqrt(a**2 + B**2 - g**2) ) / (a**2 + B**2)
    qi = atan2(si, ci)
    return (si, ci, qi)

def test_qi(qi, qi_min, qi_max, i):
    '''
    Fonction qui vérifie si un qi respecte sa valeur max et min.
    '''
    if qi > qi_max:
        raise ValueError("q" + i + " > q" + i + " max")
    elif qi < qi_min:
        raise ValueError("q" + i + " < q" + i + " min")

def MGI(xyz, m, t34, E1 = -1, E3 = 1, qi_min = [-inf, -inf, -inf], qi_max = [inf, inf, inf], qi_prev = [0, 0, 0]):
    '''
    Fonction permettant de calculer un qi d'une position selon le point xyz à atteindre.

    Parameters
    ----------
    xyz : list de float
        Liste des position x, y, z : [x, y, z].
    m : float
        Valeur du paramètre m du robot.
    t34 : np.array() 4x4
        Matrice homogène t34.
    E1 : int 1 ou -1, optional
        Valeur de l'erreur E1. The default is -1.
    E3 : int 1 ou -1, optional
        Valeur de l'erreur E3. The default is 1.
    qi_min : list de float, optional
        Liste des valeurs minimales des qi : [q1min, q2min, q3min]. The default is [-inf, -inf, -inf].
    qi_max : list de float, optional
        Liste des valeurs maximalex des qi : [q1min, q2min, q3min]. The default is [inf, inf, inf].
    qi_prev : list de float, optional
        Liste des valeur précedente des qi (postion avant déplacement) : [q1, q2, q3]. The default is [0, 0, 0].

    Raises
    ------
    ValueError
        Erreur lorsque la postition est impossible pour le robot avec les paramètres donnés.

    Returns
    -------
    q1 : float
        Valeur du q1 pour cette configuration.
    q2 : float
        Valeur du q2 pour cette configuration.
    q3 : float
        Valeur du q3 pour cette configuration.

    '''
    x,y,z = xyz         # Récupération des coordonées x, y et z (P de T04).
    
    t34x, t34y, t34z = t34[:3, 3]   # Récupération de la matrice P de T34.
    
    
    # Calcul de q1
    
    q1 = s1 = c1 = 0
    
    if x == 0 and y == 0 and t34z == 0: # Singularité, q1 n'a pas d'importance dans cette position
        q1 = qi_prev[0]                 # On choisie de ne pas modifier q1
        s1 = sin(q1)
        c1 = cos(q1)
        
    elif  x**2 + y**2 >= t34z**2:       # On peut appliquer la formule
        s1, c1, q1 = get_qi(x, y, t34z, E1)
        
    else:                               # Le robot ne peut pas atteindre la position voulue
        raise ValueError("Position impossible !")
    
    test_qi(q1, qi_min[0], qi_max[0], 1) # Vérifie si le q1 trouvé respecte ses limites. Sinon, retourne une exception
    
    
    # Calcul de q3
    
    q3 = s3 = c3 = 0
    
    if t34x == 0 and -t34y == 0 and z-m == 0: # Singularité, q3 n'a pas d'importance dans cette position
        q3 = qi_prev[1]                       # On choisie de ne pas modifier q3
        s3 = sin(q3)
        c3 = cos(q3)
        
    elif t34x**2 + t34y**2 >= (z-m)**2:       # On peut appliquer la formule
        s3, c3, q3 = get_qi(t34x, -t34y, z-m, E3)
        
    else:                                     # Le robot ne peut pas atteindre la position voulue
        raise ValueError("Position impossible !")
        
    test_qi(q3, qi_min[2], qi_max[2], 3)      # Vérifie si le q3 trouvé respecte ses limites. Sinon, retourne une exception
        
    
    # Calcul de q2
    q2 = y * c1 - x * s1 + s3 * t34x + c3 * t34y
    
    test_qi(q2, qi_min[1], qi_max[1], 2)     # Vérifie si le q2 trouvé respecte ses limites. Sinon, retourne une exception
    
    return (q1, q2, q3)

def MGI_opti(xyz, m, t34, qi_min = [-inf, -inf, -inf], qi_max = [inf, inf, inf], qi_prev = [0, 0, 0]):
    '''
    Fonction pour optenir le résultat du MGI avec le plus petit déplacement de qi.

    Parameters
    ----------
    xyz : list de float
        Liste des position x, y, z : [x, y, z].
    m : float
        Valeur du paramètre m du robot.
    t34 : np.array() 4x4
        Matrice homogène t34.
    qi_min : list de float, optional
        Liste des valeurs minimales des qi : [q1min, q2min, q3min]. The default is [-inf, -inf, -inf].
    qi_max : list de float, optional
        Liste des valeurs maximalex des qi : [q1min, q2min, q3min]. The default is [inf, inf, inf].
    qi_prev : list de float, optional
        Liste des valeur précedente des qi (postion avant déplacement) : [q1, q2, q3]. The default is [0, 0, 0].

    Raises
    ------
    ValueError
        Erreur lorsque la postition est impossible pour le robot avec les paramètres donnés.

    Returns
    -------
    TYPE list de float
        Liste des qi : [q1, q2, q3].

    '''
    qis = []            # Liste pour stocker les qis calculés.
    qi_distance = []    # Liste pour stocker les distances de chaque qi calculé par rapport au qi de départ.
    
    for E1 in (-1, 1):  # Boucle pour faire varier E1 et E3 pour trouver la combinaison optimale.
        for E3 in (-1, 1):
            try:    # Calcul des qi et des distances.
                qi = MGI(xyz, m, t34, E1=E1, E3=E3, qi_min=qi_min, qi_max=qi_max, qi_prev=qi_prev)
                distance = np.linalg.norm( np.subtract(qi, qi_prev) )
                
                qis.append(qi)
                qi_distance.append(distance)
            except ValueError:  # Si cette combinaison n'est pas valide on passe à la suivante.
                continue
    
    if len(qis) == 0:   # Si la liste de qi est vide, la position n'est pas atteignable.
        raise ValueError("Position impossible !")
    
    opti_index = np.argmin(qi_distance) # Récupération de l'index de la distance min
    return qis[opti_index]  # Renvoie du qi optimal