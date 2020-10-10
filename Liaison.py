import pybullet as p
from Axis import Axis

class Liaison:
    def __init__(self, robotId, liaisonIndex):
        self.liaisonIndex = liaisonIndex
        self.robotId = robotId
        self.axis = Axis(robotId, liaisonIndex)
        self.qiBtn = None
        self.qiBtnValue = 0
        self.qiDisplay = False
        self.qiAfficheur = None

    def buttonListener(self):
        self.axis.buttonListener()

        #Bouton Qi
        if self.qiBtn is not None:
            btnActualValue = p.readUserDebugParameter(self.qiBtn)
            if self.qiBtnValue < btnActualValue:  # Si la valeur précédente du bouton est > à celle actuelle on a appuyé dessus
                if self.qiDisplay:
                    self.removeQi()
                else:
                    self.displayQi()
                self.qiBtnValue = btnActualValue  # Mémorisation de la nouvelle valeur du bouton

    def displayAxeButton(self):
        self.axis.displayButton()

    def removeAxeButton(self):
        self.axis.removeButton()

    def displayQi(self):
        qi = p.getJointState(self.robotId, self.liaisonIndex)[0]
        if self.qiAfficheur is None:
            self.qiAfficheur = p.addUserDebugText("q"+str(self.liaisonIndex+1)+"="+str(round(qi,2)), [0.1 , 0.1, 0], [1, 0, 1], parentObjectUniqueId = self.robotId, parentLinkIndex = self.liaisonIndex)
        else:
            self.qiAfficheur = p.addUserDebugText("q"+str(self.liaisonIndex+1)+"="+str(round(qi,2)), [0.1 , 0.1, 0], [1, 0, 1], parentObjectUniqueId = self.robotId, parentLinkIndex = self.liaisonIndex, replaceItemUniqueId = self.qiAfficheur)
        self.qiDisplay = True
    
    def removeQi(self):
        p.removeUserDebugItem(self.qiAfficheur)
        self.qiAfficheur = None
        self.qiDisplay = False

    def updateDisplay(self):
        if self.qiDisplay: self.displayQi()

    def displayQiButton(self):
        """Affiche le bouton permettant d'afficher/retirer le qi"""
        if self.qiBtn is not None: return

        LiaisonNumber = str(self.liaisonIndex+1)
        self.qiBtn = p.addUserDebugParameter("Afficher/Retirer q" + LiaisonNumber, 1, 0, 0)

    def removeQiButton(self):
        """Retire le bouton permettant d'afficher/retirer le qi"""
        if self.btn is None: return

        p.removeUserDebugItem(self.btn)
        self.btn = None