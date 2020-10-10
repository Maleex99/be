import pybullet as p
from Axis import Axis
import numpy as np

class Outil:
    
    def __init__(self, robotId, liaisonIndex, corpIndex):
        self.corpIndex = corpIndex
        self.robotId = robotId
        self.liaisonIndex = liaisonIndex
        print(p.getJointInfo(robotId, liaisonIndex))

        self.axis = Axis(robotId, liaisonIndex)

        self.coordBtn = None
        self.coordBtnValue = 0
        self.coordDisplay = False
        self.coordAfficheur = None


    def buttonListener(self):
        self.axis.buttonListener()

        if self.coordBtn is not None:
            btnActualValue = p.readUserDebugParameter(self.coordBtn)
            if self.coordBtnValue < btnActualValue:
                if self.coordDisplay:
                    self.removeCoord()
                else:
                    self.displayCoord()
                self.coordBtnValue = btnActualValue

    def displayAxeButton(self):
        self.axis.displayButton()

    def removeAxeButton(self):
        self.axis.removeButton()

    def displayCoordButton(self):
        if self.coordBtn is not None: return
        self.coordBtn = p.addUserDebugParameter("Afficher/Retirer coord", 1, 0, 0)

    def removeCoordButton(self):
        """Retire le bouton permettant d'afficher/retirer le Coordonnee"""
        if self.coordBtn is None: return

        p.removeUserDebugItem(self.coordBtn)
        self.coordBtn = None

    def displayCoord(self):
        coord = p.getLinkState(self.robotId, self.liaisonIndex)[0]
        if self.coordAfficheur is None:
            self.coordAfficheur = p.addUserDebugText(str(np.around(coord, 2)), [0.1 , 0.1, 0], [1, 0, 1], parentObjectUniqueId = self.robotId, parentLinkIndex = self.liaisonIndex)
        else:
            self.coordAfficheur = p.addUserDebugText(str(np.around(coord, 2)), [0.1 , 0.1, 0], [1, 0, 1], parentObjectUniqueId = self.robotId, parentLinkIndex = self.liaisonIndex, replaceItemUniqueId = self.coordAfficheur)
        self.coordDisplay = True
    
    def removeCoord(self):
        p.removeUserDebugItem(self.coordAfficheur)
        self.coordAfficheur = None
        self.coordDisplay = False

    def updateDisplay(self):
        if self.coordDisplay: self.displayCoord()