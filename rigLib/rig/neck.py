"""
neck @ rig
"""
import maya.cmds as cmds

from ..base import module
from ..base import control


def build(neckJoints,
          headJnt,
          neckCurve,
          prefix='neck',
          rigScale=1.0,
          baseRig=None):
    """
    
    :param neckJoints: list(str), list of neck joints
    :param headJnt: str, head joint at the end of neck joint chain
    :param neckCurve: str, name of neck cubic curve with 5 CVs matching neck joints
    :param prefix: str, prefix to name new objects
    :param rigScale: float, scale factor for size of controls
    :param baseRig: instance of base.module.Base class
    :return: dictionary with rig module objects
    """

    # make rig module

    rigmodule = module.Module(prefix=prefix,
                              baseObject=baseRig)

    # make neck curve clusters

    neckCurveCVs = cmds.ls(neckCurve + '.cv[*]', fl=1)
    numNeckCVs = len(neckCurveCVs)
    neckCurveClusters = []

    for i in range(numNeckCVs):
        cls = cmds.cluster(neckCurveCVs[i], n=prefix + 'Cluster%d' % (i+1))[1]
        neckCurveClusters.append(cls)

    cmds.hide(neckCurveClusters)

    # parent neck curve

    cmds.parent(neckCurve, rigmodule.partsNoTransGrp)

    # make attach groups
    '''
    Because neck rig is depending on the spine rig
    The neck rig build is just behind the spine rig finished
    we need something to connect the spine rig and neck rig after neck riging finished
    attach groups are going to be the connections 
    just like some spine controls(non-existing) of spine to have the correct relation
    for neck rig
    for this character, we want to use the mainbody_Ctrl and chest_Ctrl to control the neck movement
    And the spine rig is already finished at the neck rig doing
    we need to create some groups at the right joint(neckJoints[0]) to figure out the problem
    '''
    # for body Ctrl and body movement
    bodyAttachGrp = cmds.group(n=prefix + 'BodyAttach_grp',
                               em=1, p=rigmodule.partsGrp)
    # for the neck rig base start, just like a base neckCtrl
    baseAttachGrp = cmds.group(n=prefix + 'BaseAttach_grp',
                               em=1, p=rigmodule.partsGrp)
    # for correct function of our setup, we need have the baseAttachGrp to
    # be matching the start of our neck jointChain (Orientation pivot point correct)
    cmds.delete(cmds.pointConstraint(neckJoints[0], baseAttachGrp))

    # make controls
    # headMainCtrl at the end of the neckChain
    headMainCtrl = control.Control(prefix=prefix + 'HeadMain',
                                   translateTo=neckJoints[-1],
                                   scale=rigScale*5,
                                   parent=rigmodule.controlGrp,
                                   shape='circleZ')

    headLocalCtrl = control.Control(prefix=prefix + 'HeadLocal',
                                    translateTo=headJnt,
                                    rotateTo=headJnt,
                                    scale=rigScale * 4,
                                    parent=headMainCtrl.C,
                                    shape='circleX')

    middleCtrl = control.Control(prefix=prefix + 'Middle',
                                 translateTo=neckCurveClusters[2],
                                 rotateTo=neckJoints[2],
                                 scale=rigScale*4,
                                 parent=rigmodule.controlGrp,
                                 shape='circleX')

    # attach controls

    cmds.parentConstraint(headMainCtrl.C, baseAttachGrp, middleCtrl.Off, sr=['x', 'y', 'z'], mo=1)
    cmds.orientConstraint(baseAttachGrp, middleCtrl.Off, mo=1)
    cmds.parentConstraint(bodyAttachGrp, headMainCtrl.Off, mo=1)

    # attach clusters
    cmds.parent(neckCurveClusters[3:], headMainCtrl.C)
    cmds.parent(neckCurveClusters[2], middleCtrl.C)
    cmds.parent(neckCurveClusters[:2], baseAttachGrp)

    # attach joints

    cmds.orientConstraint(headLocalCtrl.C, headJnt, mo=1)

    # make IK handle
    neckIK = cmds.ikHandle(n=prefix + '_ikh',
                           sol='ikSplineSolver',
                           sj=neckJoints[0],
                           ee=neckJoints[-1],
                           c=neckCurve,
                           ccv=0,
                           parentCurve=0)[0]

    cmds.hide(neckIK)
    cmds.parent(neckIK, rigmodule.partsNoTransGrp)

    # setup IK twist
    cmds.setAttr(neckIK + '.dTwistControlEnable', 1)
    cmds.setAttr(neckIK + '.dWorldUpType', 4)
    cmds.connectAttr(headMainCtrl.C + '.worldMatrix[0]', neckIK + '.dWorldUpMatrixEnd')
    cmds.connectAttr(baseAttachGrp + '.worldMatrix[0]', neckIK + '.dWorldUpMatrix')

    return {'module': rigmodule, 'baseAttachGrp': baseAttachGrp, 'bodyAttachGrp': bodyAttachGrp}


