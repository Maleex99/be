import pybullet as p
from Outil import Outil
from Liaison import Liaison

class Robot:
    def __init__(self, robotId, outilIndex):
        self.robotId = robotId
        self.outilIndex = outilIndex
        self.joints = []
        for liaisonIndex in range(p.getNumJoints(robotId)):
            if liaisonIndex == outilIndex:
                self.joints.append(Outil(robotId, outilIndex, outilIndex))
            else:
                self.joints.append(Liaison(robotId, liaisonIndex))
        
    def displayAxeButon(self, *indexs):
        for index in indexs:
            if index < 0:
                for joint in self.joints:
                    joint.displayAxeButton()
            elif index < len(joints):
                self.joints[index].displayAxeButton()

    def removeAxeButon(self, *indexs):
        for index in indexs:
            if index < 0:
                for joint in self.joints:
                    joint.removeAxeButton()
            elif index < len(joints):
                self.joints[index].removeAxeButton()

    def displayQiButton(self, *indexs):
        for index in indexs:
            if index < 0:
                for joint in self.joints:
                    if type(joint) is Outil: continue
                    joint.displayQiButton()
            elif index < len(joints) & index is not self.outilIndex:
                self.joints[index].displayQiButton()

    def removeQiButton(self, *indexs):
        for index in indexs:
            if index < 0:
                for joint in self.joints:
                    if type(joint) is Outil: continue
                    joint.removeQiButton()
            elif index < len(joints) & index is not self.outilIndex:
                self.joints[index].removeQiButton()
    
    def displayCoordButton(self):
        self.joints[self.outilIndex].displayCoordButton()

    def removeCoordButton(self):
        self.joints[self.outilIndex].removeCoordButton()

    def buttonListener(self):
        for joint in self.joints:
            joint.buttonListener()


