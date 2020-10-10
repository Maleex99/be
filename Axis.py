import pybullet as p
import numpy as np

class Axis:
    """Classe permettant d'afficher toute l'interface en rapport avec un axe du robot"""

    def __init__(self, robotId, axeIndex):
        """Crée un axe
        
        Paramètres:
            robotId -- int correspondant à l'id du robot
            axeIndex -- index de l'axe sur le robot
            axisType -- string "liaison" ou "outil"
        """
        self.axeIndex = axeIndex
        self.robotId = robotId
        self.display = False        #Indique si l'axe est affiché
        self.btn = None             #Bouton permettant l'affichage/le retrait de l'axe
        self.btnValue = 0

    def displayAxis(self):
        """Fait apparaitre l'axe en 3D sur le robot"""
        if self.display: return

        self.xAxis = p.addUserDebugLine([0, 0, 0], [1, 0, 0], [255, 0, 0], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.yAxis = p.addUserDebugLine([0, 0, 0], [0, 1, 0], [0, 255, 0], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.zAxis = p.addUserDebugLine([0, 0, 0], [0, 0, 1], [0, 0, 255], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.display = True

    def remove(self):
        """Enlève affichage l'axe sur le robot"""
        if not self.display: return

        p.removeUserDebugItem(self.xAxis)
        p.removeUserDebugItem(self.yAxis)
        p.removeUserDebugItem(self.zAxis)
        self.display = False
    
    def displayButton(self):
        """Affiche le bouton permettant d'afficher/retirer l'axe"""
        # Récupération du numéro de l'axe (Ox)
        if self.btn is not None: return

        axeNumber = str(self.axeIndex+1)

        #Affiche le bouton
        self.btn = p.addUserDebugParameter("Afficher/Retirer O" + axeNumber, 1, 0, 0)

    def removeButton(self):
        """Retire le bouton permettant d'afficher/retirer l'axe"""
        if self.btn is None: return

        p.removeUserDebugItem(self.btn)
        self.btn = None

    def buttonListener(self):
        """Gère les action du bouton"""
        if self.btn is None: return

        btnActualValue = p.readUserDebugParameter(self.btn)
        if self.btnValue < btnActualValue:  # Si la valeur précédente du bouton est > à celle actuelle on a appuyé dessus
            if self.display:
                self.remove()
            else:
                self.displayAxis()
            self.btnValue = btnActualValue  # Mémorisation de la nouvelle valeur du bouton
        