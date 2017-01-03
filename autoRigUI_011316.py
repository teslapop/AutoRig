import maya.cmds as cmds
import os
import math
import maya.mel

#variables that create the bones
scale = 1

jointSufix = 0
spineJointNum = 7
spineJointSize = 3*scale
legJoingNum = 3
legJointSize = 15*scale
armJoint = 3
armJointSize = 9*scale
rootOffset = 2*scale
hipOffset = 3*scale
ankleHeight= 2*scale
footToeJointSize = 1.5*scale
armJointOffset = 3*scale
fingerJoint = 4
fingerJointSize = 1.5*scale
fingerOffset = 2*scale
numOfFingers = 4
fingerSpacing = .5*scale
fingerAngle = 12.5
thumbJoint = 3
thumbJointSize = fingerJointSize
thumbAngleX = 0
thumbAngleY = -45/2
thumbAngleZ = -45/2
shoulderParentJoint = " "
currentFinger = ["pinky", "ring", "middle", "index"]
jointsAreParented = False
jointsMirrored = False
ikHipJoint = "root" #"spine_1" is also a good candidate for this spine ik base

armOffsetFromTopJoint = 0







def UI():
    if cmds.window("windowUI", exists = True):
         cmds.deleteUI("windowUI")

        
    #create the window
    window = cmds.window("windowUI", title = "AutoRiG++", w=300, h=400, mnb = False, mxb = False, sizeable = False)
    
    #creating the layout
    mainLayout = cmds.columnLayout(w = 300, h = 400)
    imagePath = cmds.internalVar(upd = True) + "icons/autoRigCC.jpg"

    cmds.image(w = 300, h = 100, image = imagePath)
   
    # project menu   
    cmds.separator(h = 1)
    
    cmds.button(label = "Skeletosynthesis!", w = 300, h = 70, c = build)    
    cmds.separator(h = 1)
    cmds.button(label = "Build Mirror / Re-Build Mirror", w = 300, h = 25, c = mirrorJoints) 

    cmds.separator(h = 1)
    cmds.button(label = "Remove Mirror", w = 100, h = 20, c = removeMirroredBones)
    
    cmds.separator(h = 1)
    cmds.button(label = "Select All Bones", w = 100, h = 20, c = selectAllBones)
    cmds.separator(h = 1)      
    #cmds.button(label = "Generate Locators!", w = 300, h = 70, c = genLocators)    
    #cmds.separator(h = 1)   
       
    cmds.button(label = "Fix Local Rotation Axis", w = 300, h = 20, c = fixLocalRotation)    
    cmds.separator(h = 1)   
    
    
        
    cmds.button(label = "Add Control Rig!", w = 300, h = 30, c = rig)    
    cmds.separator(h = 1)    
    
    

    
   # cmds.separator(h = 10)
    cmds.button(label = "NuKe Da Bones", w = 100, h = 30,backgroundColor = [255, 0, 0],  c = nukeDaBones)  
    
    
    
    cmds.showWindow(window)


    
def build(*args):

    nukeDaBones()
    global jointSufix
    global shoulderParentJoint
    
    
    
    print("Building")
    hipHeight = (legJoingNum-1)*legJointSize + ankleHeight + rootOffset
    
    # creates the spine and root

    for i in range (0, spineJointNum):
    
        if i == 0:
            cmds.joint(position = [0,(hipHeight+(i*spineJointSize)),0], n = "root")
        else:
            cmds.joint(position = [0,(hipHeight+(i*spineJointSize)),0], n = "spine_" + str(i))
        
        jointSufix = jointSufix+1
   

    cmds.select(cl = True)

    # creates leg Joints

    currentLegJoint = ["thigh", "shin", "foot"] 
    
    for j in range (0, legJoingNum):
        
        cmds.joint(position = [hipOffset,((legJoingNum*legJointSize + ankleHeight)- ((j+1)*legJointSize)),0], n = ("lf_" +currentLegJoint[j]))
    

    #creates foot
    cmds.joint(position = [hipOffset,0,footToeJointSize], n = "lf_ball")
    cmds.joint(position = [hipOffset,0,(3*footToeJointSize)], n = "lf_toe")


    cmds.select(cl = True)

    #ofsets the knee joint
    cmds.select("lf_shin", r = True)
    cmds.move(0,0,1, r = True)
    cmds.select("lf_foot", r = True)
    cmds.move(0,0,-1, r = True)
    
    
    
    #creates the arm

    shoulderParentJoint = "spine_" + str(jointSufix-armOffsetFromTopJoint-1)
    shoulderParentJointTranslateY = hipHeight + (spineJointSize * (jointSufix-armOffsetFromTopJoint-1))


    for k in range (0, armJoint):
        if k < armJoint-1:
            cmds.joint(position = [armJointOffset+(k * armJointSize),shoulderParentJointTranslateY,0], n = "lf_arm_"+ str(k+1))
        else:
        
            cmds.joint(position = [armJointOffset+(k * armJointSize),shoulderParentJointTranslateY,0], n = "lf_wrist")

            
    cmds.select(cl = True)     
    
    #creates the fingers
    
    fingerAngle
    
    for n in range (0, numOfFingers):
        for m in range (0, fingerJoint):
            currentFingerName = ("lf_" +currentFinger[n]+ "_finger_"+ str(m+1))
            cmds.joint(position = [(armJointSize * (armJoint-1) + armJointOffset)  + fingerOffset +(m * fingerJointSize),shoulderParentJointTranslateY,(n * fingerSpacing) - (2*fingerSpacing)], n = currentFingerName)

        cmds.select("lf_" +currentFinger[n]+ "_finger_1")
        print(("lf_" +currentFinger[n]+ "_finger_"+str(n+1)))
        cmds.rotate(0, ((2*fingerAngle) - (n*fingerAngle)), 0)
        cmds.select(cl=True)
    
    #creates the Thumb
    for p in range (0, thumbJoint):
            cmds.joint(position = [(armJointSize * (armJoint-1) + armJointOffset)  + (fingerOffset/2) +(p * thumbJointSize),shoulderParentJointTranslateY,(fingerOffset/2)], n = "lf_thumb_"+ str(p+1))

    cmds.select("lf_thumb_1")
    cmds.rotate(thumbAngleX, thumbAngleY, thumbAngleZ)
    cmds.select(cl=True)
    
    #ofsets the elbow joint
    cmds.select("lf_arm_2", r = True)
    cmds.move(0,0,-1, r = True)
    cmds.select("lf_wrist", r = True)
    cmds.move(0,0,1, r = True)
    
    ParentJoints()
    
    
def rig(*args):
    if(jointsMirrored):
        unParentJoints()
                
        #adds Ik Spline to spine joints
        cmds.select(ikHipJoint)
        cmds.select("spine_6", add = True)
        cmds.ikHandle(n = "Spine_IkSolver",sol = 'ikSplineSolver')
        cmds.rename("curve1", "spine_Curve")
        cmds.rename("effector1", "spine_Effector")
        #binds ik curve to two duplicated joints
        #this part duplicates and cleans the joints
        
        cmds.select("spine_6")
        cmds.duplicate(n = "shoulder_bind_joint")
        cmds.parent("shoulder_bind_joint", w = True)
        cmds.select("shoulder_bind_joint")
        cmds.rotate(0,-90,0, r = True)
        
        cmds.select(ikHipJoint)
        cmds.duplicate(n = "hip_bind_joint")
        cmds.select("hip_bind_joint")
        if(ikHipJoint != 'root' ):
            cmds.parent("hip_bind_joint",  w = True)
        cmds.pickWalk(d = 'down')
        cmds.delete()
        
        
        #this binds the curve to the control joints
        cmds.select("shoulder_bind_joint")
        cmds.select("hip_bind_joint", add = True)
        cmds.select("spine_Curve", add = True)
        cmds.SmoothBindSkin() # this should be binded to the selected joints with a ma influence of 2 but it still works like this
        #this creates the control curves and snaps them in placed
        #hip control curve
        maya.mel.eval('curve -d 1 -p -8.586044 2.072055 8.586044 -p -12.879065 -2.072055 9.948048 -p 12.879065 -2.072055 9.948048 -p 8.586044 2.072055 8.586044 -p -8.586044 2.072055 8.586044 -p -8.586044 2.072055 -8.586044 -p -12.879065 -2.072055 -9.948048 -p -12.879065 -2.072055 9.948048 -p -12.879065 -2.072055 -9.948048 -p 12.879065 -2.072055 -9.948048 -p 8.586044 2.072055 -8.586044 -p -8.586044 2.072055 -8.586044 -p 8.586044 2.072055 -8.586044 -p 8.586044 2.072055 8.586044 -p 12.879065 -2.072055 9.948048 -p 12.879065 -2.072055 -9.948048 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15;' )
        cmds.rename('curve1', 'hip_Cotrol')
        cmds.select(ikHipJoint)
        cmds.select('hip_Cotrol', add = True)
        cmds.pointConstraint(offset = [0,0,0], weight = 1)
        cmds.select('hip_Cotrol_pointConstraint1')
        cmds.Delete()

        #shoulder control curve
        cmds.duplicate('hip_Cotrol',n =  'shoulder_Control')
        cmds.select('shoulder_bind_joint')
        cmds.select('shoulder_Control', add = True)
        cmds.pointConstraint(offset = [0,0,0], weight = 1)
        cmds.select('shoulder_Control_pointConstraint1')
        cmds.Delete()
        cmds.select('shoulder_Control')
        cmds.scale(0.650436, -1, 0.650436, r = True)
        
        # this was not part of the tutorial
        #
        cmds.select('shoulder_Control')
        cmds.select('hip_Cotrol', add = True)
        cmds.FreezeTransformations()
        #
        #
        
        
        #changes rotate order to zxy on hip control
        cmds.setAttr("hip_Cotrol.rotateOrder", 2)
        cmds.setAttr("shoulder_Control.rotateOrder", 2)
        cmds.setAttr("hip_bind_joint.rotateOrder", 2)
        #cmds.setAttr("shoulder_bind_joint_parentConstraint1.rotateOrder" , 2)#not sure about this one either
        #cmds.setAttr("hip_bind_joint_parentConstraint1.rotateOrder", 2)# not sure about this one
        cmds.setAttr("shoulder_bind_joint.rotateOrder", 2)
        
        # parents the control joints to the control curves (hips and shoulders)
        cmds.select('shoulder_Control')
        cmds.select('shoulder_bind_joint', add = True)
        cmds.parentConstraint( mo = True,  weight =  1)
        cmds.select(cl = True)
        cmds.select('hip_Cotrol')
        cmds.select('hip_bind_joint', add = True)
        cmds.parentConstraint( mo = True,  weight =  1)
        #adding twist
        cmds.setAttr("Spine_IkSolver.dTwistControlEnable", 1)
        cmds.setAttr("Spine_IkSolver.dWorldUpType",  4)
        #adds the world up objects
        maya.mel.eval('connectAttr -f hip_bind_joint.worldMatrix[0] Spine_IkSolver.dWorldUpMatrix;')
        maya.mel.eval('connectAttr -f shoulder_bind_joint.worldMatrix[0] Spine_IkSolver.dWorldUpMatrixEnd;')
        
        
        maya.mel.eval('setAttr "Spine_IkSolver.dWorldUpAxis" 1;')
        maya.mel.eval('setAttr "Spine_IkSolver.dWorldUpVectorY" -1;')
        maya.mel.eval('setAttr "Spine_IkSolver.dWorldUpVectorEndY" 0;')
        maya.mel.eval('setAttr "Spine_IkSolver.dWorldUpVectorEndZ" -1;')
        


        
        #
        #
        #               I added a rotation to the spine top joint to compensate, this fixed the issue but it's not on the steps (lines 196, 197)
        #               part 3 in the tutorial at the end: 
        #               https://www.youtube.com/watch?v=ahgIOJysSHg
        #
        #               BELOW IS FK PART 4 OF TUTORIAL
     
        
     
        # this arrays are used to create secondary joints for spine FK
        cmds.select(cl = True)  
        spinesForFkSpine = ['root', 'spine_2', 'spine_4', 'spine_6']
        spinesForFkSpine = ['root', 'spine_2', 'spine_4', 'spine_6']
        namesForFkSpine = ['spineFKContro1','spineFKContro2','spineFKContro3','spineFKContro4']
        # creating secondary joints for spine FK 
        for i in range(0, 4):
            cmds.joint(position = [0,0,0], n = namesForFkSpine[i])

        for j in range(0, 4):
            cmds.select(spinesForFkSpine[j])
            cmds.select(namesForFkSpine[j], add = True)
            cmds.pointConstraint(offset = [0,0,0], weight = 1, n = 'temp')
            cmds.select('temp')
            cmds.Delete()



        
        
        
        
        
        
        

        ParentJoints()
    else:
        print("All joints must be placed before control rig is added.")
    
    
    
    
    
def mirrorJoints(*args):

    if((cmds.objExists("rg_arm_1")) and cmds.objExists("root")):
        print("Destroying Mirror")
        removeMirroredBones()
    
    if (not (cmds.objExists("rg_arm_1")) and cmds.objExists("root")):
        global jointsMirrored
        print("Mirroring Bones")
        cmds.select("lf_arm_1")
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ("lf_",  "rg_"))
        cmds.select("lf_thigh")   
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ("lf_",  "rg_"))    
        cmds.select(cl = True)
        jointsMirrored = True
        fixLocalRotation()
    elif not cmds.objExists("root"):
        print("No Bones to Mirror")

        
def removeMirroredBones(*args):
    if (not (cmds.objExists("rg_arm_1"))):
        print("No Mirrored Joints")
    else:
        global jointsMirrored
        cmds.delete("rg_arm_1")
        cmds.delete("rg_thigh")   
        cmds.select(cl = True)
        jointsMirrored = False

        
def selectAllBones(*args):


    allObjects = cmds.ls(l=True)
    
    for obj in allObjects:
    
        if cmds.nodeType(obj) == 'joint':
            cmds.select(obj, toggle = True)
          
    
def genLocators(*args):
    print("Locaators")
    cmds.spaceLocator(n = "rootLocator", p = [0, 0, 0])
    cmds.annotate("rootLocator", tx = "root_Loc", p = [2, 2, 0])
    cmds.parent(cmds.ls(sl = True),"rootLocator")
    cmds.select("rootLocator")
   
   
def fixLocalRotation(*arg):
    unParentJoints()
    currentSide = ["lf", "rg"]
    
    if(jointsMirrored):
        for i in range (0, 2):

            selectAllBones()
            cmds.FreezeTransformations()
            cmds.select("root")
            #per tutorial - secondary axis of rotation is set to X no default Y
            cmds.joint( e = True  ,oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)
            cmds.select(currentSide[i] + "_arm_1")
            cmds.joint( e = True  ,oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)
            cmds.select(currentSide[i] + "_thigh")
            cmds.joint( e = True  ,oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)
            cmds.select(currentSide[i] + "_thumb_1") 
            cmds.joint( e = True  ,oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)
            #parents the finger joints    
            for n in range (0, numOfFingers):
                cmds.select(currentSide[i] + "_" +currentFinger[n]+ "_finger_1")
                cmds.joint( e = True  ,oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)
    else:
        print("Joints must be mirrored")

    cmds.select(cl = True)
    ParentJoints()

       
def ParentJoints(*arg):  
    global jointsAreParented
    
    if(not jointsAreParented):
  
        #parents all the joints
        cmds.parent("lf_arm_1",shoulderParentJoint)
        cmds.parent("lf_thigh","root")
        cmds.parent("lf_thumb_1", "lf_wrist") 
        #parents the finger joints    
        for n in range (0, numOfFingers):
            cmds.parent("lf_" +currentFinger[n]+ "_finger_1", "lf_wrist")
            
        if(jointsMirrored):
            #parents all mirrored joints
            cmds.parent("rg_arm_1",shoulderParentJoint)
            cmds.parent("rg_thigh","root")
            cmds.parent("rg_thumb_1", "rg_wrist") 
            #parents the finger joints    
            for n in range (0, numOfFingers):
                cmds.parent("rg_" +currentFinger[n]+ "_finger_1", "rg_wrist")
       
        cmds.select(cl = True)
        jointsAreParented = True
    else:
        unParentJoints()


def unParentJoints(*arg):   
    global jointsAreParented
    
    #parents all the joints
    cmds.parent("lf_arm_1", w = True)
    cmds.parent("lf_thigh", w = True)
    cmds.parent("lf_thumb_1", w = True) 
    #parents the finger joints    
    for n in range (0, numOfFingers):
        cmds.parent("lf_" +currentFinger[n]+ "_finger_1", w = True)
    if(jointsMirrored):    
        #parents all the joints
        cmds.parent("rg_arm_1", w = True)
        cmds.parent("rg_thigh", w = True)
        cmds.parent("rg_thumb_1", w = True) 
        #parents the finger joints    
        for n in range (0, numOfFingers):
            cmds.parent("rg_" +currentFinger[n]+ "_finger_1", w = True)

    cmds.select(cl = True)
    jointsAreParented = False


def nukeDaBones(*args):

    global jointSufix
    global jointsAreParented
    global jointsMirrored


    jointSufix = 0
    jointsAreParented = False
    jointsMirrored = False


    for i in range (0, 100):

        allObjects = cmds.ls(l=True)

    
        for obj in allObjects:
        

            if cmds.nodeType(obj) == 'joint':
               cmds.delete(obj)
               break
     



