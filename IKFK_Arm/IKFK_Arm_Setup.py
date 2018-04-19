"""
IKFK Spine rig setup
main modue
"""

import sys
import project
from rigLib.rig import IK_FK_Arm

import maya.cmds as cmds

sys.path.append('C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/python')


sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = None

builderSceneFilePath = '%s/%s/builder/%s_builder.mb'

def build(characterName):
    """
    main function to build IKFK Spine rig
    :param characterName: str, characterName
    :return: None
    """

    # new Scene
    cmds.file(new=1, force=1)

    # import builder Scene
    builderFile = 'C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/python/assets/IKFK_Arm/builder/IKFK_Arm_builder.mb'
    cmds.file(builderFile, i=1)

    # make controlSetup
    makeControlSetup()


def makeControlSetup():
    topJoint = 'l_clavicle'
    startDupJnt = 'l_shouder'
    endDupJnt = 'l_wrist'
    prefix = 'l_'
    armPvLoc = 'armPvLoc'
    switchCtrlLoc ='switchCtrlLoc'

    # call build function in IK_FK_Arm
    IK_FK_Arm.build(topJoint=topJoint,
                    startDupJnt=startDupJnt,
                    endDupJnt=endDupJnt,
                    prefix=prefix,
                    armPvLoc=armPvLoc,
                    switchCtrlLoc=switchCtrlLoc,
                    rigScale=sceneScale,
                    fkPreParent=None)
