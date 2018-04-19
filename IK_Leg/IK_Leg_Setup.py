"""
IK LEG rig setup
main module
"""

import sys

from . import project

from ..rigLib.rig import IK_Leg

import maya.cmds as cmds


sys.path.append('C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/python')

sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = None

builderSceneFilePath = '%s/%s/builder/%s_builder.mb'



def builder(characterName):
    """
    main function to build IK leg rig
    :param characterName: characterName:str,
    :return: 
    """
    # new Scene
    cmds.file(new=1, force=1)

    # import builder Scene
    # builderFile = builderSceneFilePath % (mainProjectPath, characterName, characterName)
    builderFile = 'C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/assets/IK_LEG/builder'
    cmds.file(builderFile, i=1)

    # make controlSetup
    makeControlSetup()



def makeControlSetup():

    topJoint = 'L_Skin_hip'
    pvLocator = 'pvLocator'
    revLocator = ['CBank_LOC', 'EBank_LOC', 'Heel_LOC', 'Pivot_LOC']
    rollLocator = 'rollLocator'

    IK_Leg.build(topJoint=topJoint,
                 pvLocator=pvLocator,
                 revLocator=revLocator,
                 prefix='L_',
                 rigScale=sceneScale*5,
                 rollCtrlLOC=rollLocator)
