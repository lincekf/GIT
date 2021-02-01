import maya.cmds as cmds

sele = cmds.ls(selection = True)


if len(sele) != 1:
    raise ValueError ('please select only one object')


sele_shape = cmds.listRelatives(sele, shapes = True)

if not cmds.objectType(sele_shape) == 'camera':
    raise ValueError("The selection should be a single camera")

# storing the start and end frames of a time slider. 
StartTime = cmds.playbackOptions(q = True, animationStartTime = True)
EndTime = cmds.playbackOptions(q = True, animationEndTime = True)




def cam_bake():

    # creating a fresh camera 
    new_cam,new_cam_shape = cmds.camera(n = 'MM_camera')
    
    # parenting that camera with the selected camera  
    parent_newcam_node = cmds.parentConstraint(sele, new_cam, maintainOffset = False)


    # copying the selected camera image plane values including the sequence path and pasting that in to a newly created image plane which is connected to the new camera. 
    # If no source image available then its directly move on to the bake process. 
    source_image = cmds.listRelatives(cmds.listRelatives(sele))
    if source_image:
        source_image_shape = cmds.listRelatives(source_image)
        source_image_path = cmds.getAttr('%s.imageName' %source_image[0])    
       
        new_cam_image, new_cam_image_shape = cmds.imagePlane(camera = new_cam, fileName = source_image_path)
        cmds.copyAttr( source_image_shape, new_cam_image_shape, inConnections = True, values = True)
        cmds.setAttr ('%s.useFrameExtension'  %new_cam_image_shape, 0)

    # baking the new camera channels and deleting the constraint. 
    cmds.bakeResults( new_cam , time=(StartTime,EndTime) )
    cmds.delete(parent_newcam_node)
    
    # will enable the Image sequence option inside image plane. 
    if source_image:
        cmds.setAttr ('%s.useFrameExtension'  %new_cam_image_shape, 1)

    # transferring the camera setting 
    cmds.copyAttr( sele_shape,new_cam_shape,values = True)

    # cheching for any curves inside the camera shape, this is mainly to get the focal curve incase if available. And pasting that in to the new camera. 
    copy_keys = cmds.copyKey(sele_shape)
    if copy_keys:
        cmds.pasteKey(new_cam_shape)
    
    # creating a new group for the newly created camera. Add that under this group. 
    Render_camera_grp = cmds.group(n = 'RenderCamGroup', empty = True)
    cmds.parent(new_cam, Render_camera_grp)

    # locking the attributes. 
    cam_attr = ['translate', 'rotate', 'scale', 'focalLength', 'horizontalFilmAperture', 'verticalFilmAperture' ]

    for attr in cam_attr:
        cmds.setAttr('%s.%s' % (new_cam, attr) , lock = True)
    for i in range (0,3):
        cmds.setAttr('%s.%s' % (Render_camera_grp, cam_attr[i]) , lock = True)

    
    
    




cam_bake()








