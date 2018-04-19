"""
komodo dragon rig setup
deformation setup
"""
from . import project
import maya.cmds as cmds
import maya.mel as mel
import os
from rigTools import bSkinSaver
from rigLib.utils import name


skinWeightsDir = 'weights/skinCluster'

swExt = '.swt'
bodyGeo = 'body_geo'
bodyMidresGeo = 'body_midres_geo'

def build(baseRig, characterName):

    modelGrp = '%s_model_grp' % characterName

    #make twist joints
    refTwistJoints = ['l_elbow1_jnt', 'l_knee1_jnt', 'r_elbow1_jnt', 'r_knee1_jnt']
    maketwistJoints(baseRig, refTwistJoints)

    #load skinweights
    geoList = _getModelGeoObjects(modelGrp)
    loadSkinWeights(characterName, geoList)

    #apply mush deformer
    _applyDeltaMush(bodyMidresGeo)

    #wrap hires body mesh

    _makeWrap([bodyGeo], bodyMidresGeo)


def _makeWrap(wrappedObjs, wrapperObj):

    cmds.select(wrappedObjs)
    cmds.select(wrapperObj, add=1)
    mel.eval('doWrapArgList "7" {"1", "0", "1", "2", "1", "1", "0", "0"}')


def _applyDeltaMush(geo):

    deltaMushDf = cmds.deltaMush(geo, smoothingIterations=50)


def _getModelGeoObjects(modelGrp):
    geoList = [cmds.listRelatives(o, p=1)[0] for o in cmds.listRelatives(modelGrp, ad=1, type='mesh')]

    return geoList


def maketwistJoints(baseRig, parentJoints):

    twistJointsMainGrp = cmds.group(n='twistJoints_grp', p=baseRig.jointGrp, em=1)

    for parentJnt in parentJoints:
        prefix = name.removeSuffix(parentJnt)

        # remove the number in prefix
        prefix = prefix[:-1]

        parentjntChild = cmds.listRelatives(parentJnt, c=1, type='joint')[0]

        # make twist joints
        twistJntGrp = cmds.group(n=prefix + 'twistJoint_grp', p=twistJointsMainGrp, em=1)

        twistParentJnt = cmds.duplicate(parentJnt, n=prefix + 'Twist1_jnt', parentOnly=1)[0]
        twistChildJnt = cmds.duplicate(parentjntChild, n=prefix + 'Twist2_jnt', parentOnly=1)[0]

        # adjust twist joints

        origJntRadius = cmds.getAttr(parentJnt + '.radius')
        for j in [twistParentJnt, twistChildJnt]:
            cmds.setAttr(j + '.radius', origJntRadius * 2)
            cmds.color(j, ud=1)

        cmds.parent(twistChildJnt, twistParentJnt)
        cmds.parent(twistParentJnt, twistJntGrp)

        #attach twist joints
        cmds.pointConstraint(parentJnt, twistParentJnt)

        #make IK handle
        twistIK = cmds.ikHandle(n=prefix + 'TwistJoint_ikh',
                                solver='ikSCsolver',
                                startJoint=twistParentJnt,
                                endEffector=twistChildJnt)[0]

        cmds.hide(twistIK)
        cmds.parent(twistIK, twistJntGrp)
        cmds.parentConstraint(parentjntChild, twistIK)


def saveSkinWeights(characterName, geoList=[]):
    '''
    save weights for character geometry objects
    :param characterName: 
    :param geoList: 
    :return: 
    '''

    for obj in geoList:
        #weights file

        wtFile = os.path.join(project.mainProjectPath, characterName, skinWeightsDir, obj + swExt)

        #save skin weight file
        cmds.select(obj)
        bSkinSaver.bSaveSkinValues(wtFile)


def loadSkinWeights(characterName, geoList=[]):

    '''
    load skin weights for character geometry objects
    :param characterName: 
    :param geoList: 
    :return: 
    '''

    # weights folders
    wtDir = os.path.join(project.mainProjectPath, characterName, skinWeightsDir)

    wtFiles = os.listdir(wtDir)

    # load skin weights
    for wtFile in wtFiles:
        extRes = os.path.splitext(wtFile)

        # check extension format
        # use continue to jump out of this time loop
        if not extRes > 1:
            continue

        # check skin weight file
        if not extRes[1] == swExt:
            continue

        # check geometry list
        if geoList and not extRes[0] in geoList:
            continue

        # check if objects exist
        if not cmds.objExists(extRes[0]):
            continue

        # load skin weight
        fullpathWtFile = os.path.join(wtDir, wtFile)
        bSkinSaver.bLoadSkinValues(loadOnSelection=False, inputFile=fullpathWtFile)

