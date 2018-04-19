"""
IKFK Spine rig setup
main modue
"""

import sys
from . import project
from ..rigLib.rig import IK_FK_Spine

import maya.cmds as cmds

sys.path.append('C:/Users/user/Documents/maya/2017/scripts/KOMODO/code/python')


sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = None

builderSceneFilePath = '%s/%s/builder/%s_builder.mb'

def builder(characterName):
    """
    main function to build IKFK Spine rig
    :param characterName: str, characterName
    :return: None
    """

    # new Scene
    cmds.file(new=1, force=1)

    # import builder Scene
    builderFile = 'C:/Users/tHeBeStXu/Documents/maya/projects/assets/IKFK_Spine/builder/IKFK_Spine_builder.mb'
    cmds.file(builderFile, i=1)

    # make controlSetup
    makeControlSetup()


def makeControlSetup():

    spineJoints = ['C_Spine_0', 'C_Spine_1', 'C_Spine_2', 'C_Spine_3', 'C_Spine_4', 'C_Spine_5']
    fkSpineCrv = 'fkSpine_Crv'

    IK_FK_Spine.build(spineJoints=spineJoints,
                      fkSpineCrv=fkSpineCrv,
                      prefix='C_Spine',
                      rigScale=sceneScale*5)
