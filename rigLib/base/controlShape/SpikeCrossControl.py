import maya.cmds as cmds


def createShape(prefix='', scale=1.0):

    List = []
    List.append(cmds.curve(n=prefix + '_ctl', p=[(0.5698271508338371, 4.091121663662989e-09, -2.132883735050939e-05), (0.4208952391731131, 0.1488873944517639, -1.5755096100633637e-05), (0.2720931419242101, 4.073556049855043e-05, -1.0184545420344193e-05), (0.4209398007112384, -0.1487613617926744, -1.5755096101521815e-05), (0.5698271508338371, 4.091121663662989e-09, -2.132883735050939e-05), (0.42091194939155674, 6.301549556786412e-05, -0.1488401347819135), (0.2720931419242101, 4.073556049855043e-05, -1.0184545420344193e-05), (0.42092309049279564, 6.301716352297149e-05, 0.14880862458971134), (0.5698271508338371, 4.091121663662989e-09, -2.132883735050939e-05), (0.4208952391731131, 0.1488873944517639, -1.5755096100633637e-05), (0.2720931419242101, 4.073556049855043e-05, -1.0184545420344193e-05), (-0.2720931291529265, -0.0001260413294232876, 1.0184545417679658e-05), (-0.4209971894939688, -6.30282570215357e-05, 0.14884013797247952), (-0.5698271380625544, -8.530986004595675e-05, 2.1328837348733032e-05), (-0.4210083305952077, -6.302992497664306e-05, -0.1488086213991462), (-0.2720931291529265, -0.0001260413294232876, 1.0184545417679658e-05), (-0.42085456057731463, 0.14876116408473417, 1.5751905531047328e-05), (-0.5698271380625544, -8.530986004595675e-05, 2.1328837348733032e-05), (-0.4209804792755252, -0.14888740721321847, 1.575828666666723e-05), (-0.2720931291529265, -0.0001260413294232876, 1.0184545417679658e-05), (-0.2720931291529265, -0.0001260413294232876, 1.0184545417679658e-05), (0.0, -1.3322676295501878e-15, 0.0), (-1.1141101238898443e-05, -1.6679564396326896e-09, 0.2721144031802565), (0.00014271626145045957, 0.14882419235483146, 0.42093877648166433), (0.0, -1.3322676295501878e-15, 0.569763162551884), (1.671021844362741e-05, -0.14882437895619827, 0.42093878286606934), (-1.1141101238898443e-05, -1.6679564396326896e-09, 0.2721144031802565), (-0.14882987953462568, -2.2281592690021057e-05, 0.4209443534141677), (0.0, -1.3322676295501878e-15, 0.569763162551884), (0.14890412937122033, -6.29878057401001e-05, 0.42093320912223664), (-1.1141101238898443e-05, -1.6679564396326896e-09, 0.2721144031802565), (-3.151178319171777e-05, -4.717688018018862e-09, -0.2721144015837451), (-5.935678879254169e-05, 0.14882437257149927, -0.4209387812697942), (-4.265288443061621e-05, -6.385641793116292e-09, -0.5697631609553717), (-1.4801564748090357e-05, -0.1488243836738845, -0.42093878126955797), (-3.151178319171777e-05, -4.717688018018862e-09, -0.2721144015837451), (-0.1488613913178174, -2.2286310378039076e-05, -0.4209332107214614), (-4.265288443061621e-05, -6.385641793116292e-09, -0.5697631609553717), (0.1488726175880286, -6.299252342767403e-05, -0.42094435501339156), (-3.151178319171777e-05, -4.717688018018862e-09, -0.2721144015837451)],per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]))
    for x in range(len(List)-1):
        cmds.makeIdentity(List[x+1], apply=True, t=1, r=1, s=1, n=0)
        shapeNode = cmds.ListRelatives(List[x+1], shapes=True)
        cmds.parent(shapeNode, List[0], add=True, s=True)
        cmds.delete(List[x+1])
    sel = List[0]
    cmds.setAttr(sel + '.s', scale, scale, scale)
    cmds.makeIdentity(sel, apply=1, t=1, r=1, s=1, n=0)
    return sel