import sys
from . import project


from ..rigLib.rig import IK_FK_Arm
from ..rigLib.rig import IK_FK_Spine

import maya.cmds as cmds

sys.path.append('C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/python')

sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = None

builderSceneFilePath = '%s/%s/builder/%s_builder.mb'

def builder(characterName):
    """
    
    :param characterName: 
    :return: 
    """
    # new Scene
    cmds.file(new=1, force=1)

    # import builder Scene
    # builderFile = builderSceneFilePath % (mainProjectPath, characterName, characterName)


    builderFile = 'C:\Users\user/Documents/maya/2017/scripts/KOMODO/code/assets/humanRig/builder/humanRig_builder.mb'


    cmds.file(builderFile, i=1)

    # make controlSetup
    makeControlSetup()


def makeControlSetup():

    # SPINE
    spineJoints = ['C_Spine_0', 'C_Spine_1', 'C_Spine_2', 'C_Spine_3', 'C_Spine_4', 'C_Spine_5', 'C_Spine_6']
    fkSpineCrv = 'fkSpine_Crv'
    prefix = 'C_Spine'

    spineRig = IK_FK_Spine.build(spineJoints=spineJoints,
                                 fkSpineCrv=fkSpineCrv,
                                 prefix=prefix,
                                 rigScale=sceneScale * 5)

    # LEFT ARM
    topJoint = 'l_clavicle'
    startDupJnt = 'l_shouder'
    endDupJnt = 'l_wrist'
    prefix = 'l_arm_'
    armPvLoc = 'armPvLoc'
    switchCtrlLoc = 'switchCtrlLoc'

    # call build function in IK_FK_Arm
    l_armRig = IK_FK_Arm.build(topJoint=topJoint,
                               startDupJnt=startDupJnt,
                               endDupJnt=endDupJnt,
                               prefix=prefix,
                               armPvLoc=armPvLoc,
                               switchCtrlLoc=switchCtrlLoc,
                               rigScale=sceneScale*5,
                               fkPreParent=None)

    cmds.parentConstraint(spineJoints[-1], l_armRig['baseAttachGrp'], mo=1)
    cmds.parentConstraint(spineRig['spineBodyCtrl'].C, l_armRig['bodyAttachGrp'], mo=1)
