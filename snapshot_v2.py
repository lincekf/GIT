import maya.cmds as cmds


def check_panel(cam_name):
    
    pan = cmds.getPanel( type="modelPanel" )
    for p in pan:
        mod = cmds.modelEditor(p, query = True, camera = True)
        if mod == '%s' % cam_name:
            global given_panel 
            given_panel = p
            
            
                
def snapshot(name, view):
    
    check_panel(view)
    
    path = cmds.internalVar(userAppDir = True)
    time = cmds.currentTime( query=True )    
    fullpath = os.path.join(path, '%s.jpeg' %name)
    
    cmds.setAttr ("defaultRenderGlobals.imageFormat" , 8 )
    
    cmds.playblast( editorPanelName = '%s' %given_panel, completeFilename = fullpath, forceOverwrite = True, format = 'image', startTime = time , endTime = time, width = 256, height = 256, viewer = False, showOrnaments = False )


snapshot('scene_snap', 'persp')