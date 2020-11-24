import numpy as np

def MGD(qi, m):
    '''
    Fonction pour calculer un MGD

    Parameters
    ----------
    qi : list de float
        Liste des qi : [q1, q2, q3].
    m : float
        Valeur du paramètre m du robot.

    Returns
    -------
    result : list de float
        Liste des positions x, y, z du robot : [x, y, z].

    '''

    #q list
    q1 = qi[0]
    q2 = qi[1]
    q3 = qi[2]

    #cos(q)
    c1 = np.cos(q1)
    c3 = np.cos(q3)

    #sin(q)
    s1 = np.sin(q1)
    s3 = np.sin(q3)

    #fill T03 : left -> right | top -> bottom
    result = np.zeros((4,4))

    result[0][0] = s3 * s1
    result[0][1] = s1 * c3
    result[0][2] = c1
    result[0][3] = (-1) * s1 * q2

    result[1][0] = (-1) * s3 * c1
    result[1][1] = (-1) * c1 * c3
    result[1][2] = s1
    result[1][3] = c1 * q2

    result[2][0] = c3
    result[2][1] = (-1) * s3
    result[2][3] = m

    result[3][3] = 1
    
    return result