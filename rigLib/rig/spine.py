'''
spine @ rig
'''

import maya.cmds as cmds

from ..base import module
from ..base import control

def build(spineJoints,
          rootJnt,
          spineCurve,
          bodyLocator,
          chestLocator,
          pelvisLocator,
          prefix='spine',
          rigScale=1.0,
          baseRig=None):
    '''
    
    :param spineJoints: list(str), list fo 6 spine joints
    :param rootJnt: str,root joint
    :param spineCurve: str, name of spine cubic curve with 5 CVs matching 5 spine joints
    :param bodyLocator: str, reference transform for position of body control
    :param chestLocator: str, reference transform for position of chest control
    :param pelvisLocator: str, reference transform for position of pelvis control
    :param prefix: str, prefix to name new objects
    :param rigScale: float, scale factor for size of controls
    :param baseRig: instance of base.module.Base class
    :return: dictionary with rig module objects
    '''

    # make rig module

    rigmodule = module.Module(prefix=prefix, baseObject=baseRig)

    # make spine curve clusters
    spineCurveCVs = cmds.ls(spineCurve + '.cv[*]', fl=1)
    numSpineCVs = len(spineCurveCVs)
    spineCurveClusters = []

    for i in range(numSpineCVs):

        cls = cmds.cluster(spineCurveCVs[i], n=prefix + 'Cluster%d' % (i+1))[1]

        spineCurveClusters.append(cls)

    cmds.hide(spineCurveClusters)

    # parent spine curve

    cmds.parent(spineCurve, rigmodule.partsNoTransGrp)
    # make controls

    bodyCtrl = control.Control(prefix=prefix+'Body',
                               translateTo=bodyLocator,
                               scale=rigScale*4,
                               parent=rigmodule.controlGrp)

    chestCtrl = control.Control(prefix=prefix + 'Chest',
                                translateTo=chestLocator,
                                scale=rigScale * 6,
                                shape='circleZ',
                                parent=bodyCtrl.C
                                )

    pelvisCtrl = control.Control(prefix=prefix + 'Pelvis',
                                 translateTo=pelvisLocator,
                                 scale=rigScale * 6,
                                 parent=bodyCtrl.C,
                                 shape='circleZ')

    middleCtrl = control.Control(prefix=prefix + 'Middle',
                                 translateTo=spineCurveClusters[2],
                                 scale=rigScale * 3,
                                 parent=bodyCtrl.C,
                                 shape='circleZ')

    _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale)

    # attach controls
    cmds.parentConstraint(chestCtrl.C, pelvisCtrl.C, middleCtrl.Off, sr=['x', 'y', 'z'], mo=1)

    # attach clusters
    cmds.parent(spineCurveClusters[3:], chestCtrl.C)
    cmds.parent(spineCurveClusters[2], middleCtrl.C)
    cmds.parent(spineCurveClusters[:2], pelvisCtrl.C)

    # attach chest joint
    cmds.orientConstraint(chestCtrl.C, spineJoints[-2], mo=1)

    # make IK handle
    spineIK = cmds.ikHandle(n=prefix + '_ikh',
                            sol='ikSplineSolver',
                            sj=spineJoints[0],
                            ee=spineJoints[-2],
                            c=spineCurve,
                            ccv=0,
                            parentCurve=0)[0]

    cmds.hide(spineIK)
    cmds.parent(spineIK, rigmodule.partsNoTransGrp)

    # setup IK twist
    cmds.setAttr(spineIK + '.dTwistControlEnable', 1)
    cmds.setAttr(spineIK + '.dWorldUpType', 4)
    cmds.connectAttr(chestCtrl.C + '.worldMatrix[0]', spineIK + '.dWorldUpMatrixEnd')
    cmds.connectAttr(pelvisCtrl.C + '.worldMatrix[0]', spineIK + '.dWorldUpMatrix')

    # attach root joint
    cmds.parentConstraint(pelvisCtrl.C, rootJnt, mo=1)

    return {'module': rigmodule, 'bodyCtrl': bodyCtrl}


def _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale):
    """
    offset body control along spine Y axis
    :param bodyCtrl: 
    :param spineJoints: 
    :param rigScale: 
    :return: None
    """

    # create a empty group at bodyCtrl.C location and parent it to bodyCtrl.C
    offsetGrp = cmds.group(em=1, p=bodyCtrl.C)
    cmds.parent(offsetGrp, spineJoints[2])

    ctrCls = cmds.cluster(cmds.listRelatives(bodyCtrl.C, s=1))[1]

    cmds.parent(ctrCls, offsetGrp)

    cmds.move(10*rigScale, offsetGrp, moveY=1, relative=1, objectSpace=1)

    cmds.delete(bodyCtrl.C, ch=1)


