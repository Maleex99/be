import pybullet as p
import time
import pybullet_data
from math import pi
import numpy as np

class Axis:
    """Classe permettant d'afficher toute l'interface en rapport avec un axe du robot"""

    def __init__(self, robotId, axeIndex, axisType = "liaison"):
        """Crée un axe
        
        Paramètres:
            robotId -- int correspondant à l'id du robot
            axeIndex -- index de l'axe sur le robot
            axisType -- string "liaison" ou "outil"
        """
        self.axeIndex = axeIndex
        self.robotId = robotId
        self.startPos = []          #utile pour bien positionner l'axe de l'outil
        self.display = False        #Indique si l'axe est affiché
        self.btn = None             #Bouton permettant l'affichage/le retrait de l'axe
        self.axisType = axisType    #Indique si c'est une liaison ou un outil
        self.btnValue = 0
        if axisType == "liaison":
            self.startPos = [0, 0, 0]
        elif axisType == "outil":
            self.startPos = [0, -1, 0]

    def displayAxis(self):
        """Fait apparaitre l'axe en 3D sur le robot"""
        self.xAxis = p.addUserDebugLine(self.startPos, np.array(self.startPos) + [1, 0, 0], [255, 0, 0], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.yAxis = p.addUserDebugLine(self.startPos, np.array(self.startPos) + [0, 1, 0], [0, 255, 0], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.zAxis = p.addUserDebugLine(self.startPos, np.array(self.startPos) + [0, 0, 1], [0, 0, 255], parentObjectUniqueId = self.robotId, parentLinkIndex = self.axeIndex)
        self.display = True

    def remove(self):
        """Enlève affichage l'axe sur le robot"""
        p.removeUserDebugItem(self.xAxis)
        p.removeUserDebugItem(self.yAxis)
        p.removeUserDebugItem(self.zAxis)
        self.display = False
    
    def displayButton(self):
        """Affiche le bouton permettant d'afficher/retirer l'axe"""
        # Récupération du numéro de l'axe (Ox)
        axeNumber = -1
        if self.axisType == "liaison":
            axeNumber = str(axeIndex+1)
        else:
            axeNumber = str(axeIndex+1+1)

        #Affiche le bouton
        self.btn = p.addUserDebugParameter("Afficher/Retirer O" + axeNumber, 1, 0, 0)

    def removeButton(self):
        """Retire le bouton permettant d'afficher/retirer l'axe"""
        if self.btn is None: return

        p.removeUserDebugItem(self.btn)
        self.btn = None

    def checkButton(self):
        """Gère les action du bouton"""
        btnActualValue = p.readUserDebugParameter(self.btn)
        if self.btnValue < btnActualValue:  # Si la valeur précédente du bouton est > à celle actuelle on a appuyé dessus
            if self.display:
                self.remove()
            else:
                self.displayAxis()
            self.btnValue = btnActualValue  # Mémorisation de la nouvelle valeur du bouton
        

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
    p.setGravity(0, 0, -10)
    planeId = p.loadURDF("plane.urdf")
    cubeStartPos = [0, 0, 0]
    cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
    
    # Parametres
    q1ParamSlider = p.addUserDebugParameter("q1", -pi, pi, 0)
    q2ParamSlider = p.addUserDebugParameter("q2", 0, 1, 0)
    q3ParamSlider = p.addUserDebugParameter("q3", -pi, pi, 0)

    # Bouton axis
    btYZ = p.addUserDebugParameter("Calculer MGD YZ",1,0,0)
    btYZvalue = 0
    
    robotId = p.loadURDF("robot_be.urdf", cubeStartPos, cubeStartOrientation)

    # Création axes
    axis = []
    nbJoin = p.getNumJoints(robotId)
    for axeIndex in range(nbJoin):
        axis.append(Axis(robotId, axeIndex))
        axis[axeIndex].displayButton()
    axis.append(Axis(robotId, nbJoin-1, "outil"))
    axis[nbJoin].displayButton()


    for i in range(10000):
        # Recuperation des valeurs des sliders
        q1Param = p.readUserDebugParameter(q1ParamSlider)
        q2Param = p.readUserDebugParameter(q2ParamSlider)
        q3Param = p.readUserDebugParameter(q3ParamSlider)

        # Application des qis
        p.setJointMotorControl2(robotId,0,p.POSITION_CONTROL,targetPosition=q1Param)
        p.setJointMotorControl2(robotId,1,p.POSITION_CONTROL,targetPosition=q2Param)
        p.setJointMotorControl2(robotId,2,p.POSITION_CONTROL,targetPosition=q3Param)

        # Check Axis buttons
        for axe in axis:
            axe.checkButton()

        p.stepSimulation()
        time.sleep(1. / 240.)
    cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
    print(cubePos, cubeOrn)
    p.disconnect()
