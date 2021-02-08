import maya.cmds as cmds

def snapshot(name):
    path = cmds.internalVar(userAppDir = True)
    time = cmds.currentTime( query=True )    
    fullpath = os.path.join(path, '%s.jpeg' %name)
    
    cmds.setAttr ("defaultRenderGlobals.imageFormat" , 8 )
    
    cmds.playblast(completeFilename = fullpath, forceOverwrite = True, format = 'image', startTime = time , endTime = time, width = 256, height = 256, viewer = False, showOrnaments = False )


snapshot('scene_snap')