import pybullet as p
import time
import pybullet_data
from math import pi
import numpy as np
from Robot import Robot

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
    
    robotId = p.loadURDF("robot_be.urdf", cubeStartPos, cubeStartOrientation)   

    robot = Robot(robotId, 3)
    robot.displayAxeButon(-1)
    robot.displayQiButton(-1)
    robot.displayCoordButton()


    for i in range(10000):
        # Recuperation des valeurs des sliders
        q1Param = p.readUserDebugParameter(q1ParamSlider)
        q2Param = p.readUserDebugParameter(q2ParamSlider)
        q3Param = p.readUserDebugParameter(q3ParamSlider)

        # Application des qis
        p.setJointMotorControl2(robotId,0,p.POSITION_CONTROL,targetPosition=q1Param)
        p.setJointMotorControl2(robotId,1,p.POSITION_CONTROL,targetPosition=q2Param)
        p.setJointMotorControl2(robotId,2,p.POSITION_CONTROL,targetPosition=q3Param)

        # Check buttons
        robot.buttonListener()

        p.stepSimulation()
        time.sleep(1. / 240.)
    cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
    print(cubePos, cubeOrn)
    p.disconnect()
