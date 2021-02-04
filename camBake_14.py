import maya.cmds as cmds

sele = cmds.ls(selection = True)


# storing the start and end frames of a time slider. 
StartTime = cmds.playbackOptions(q = True, animationStartTime = True)
EndTime = cmds.playbackOptions(q = True, animationEndTime = True)


# checking some basic conditions first. This function will make sure, artist selected only One single camera. 
def validate_selection(selected_objects):
    if len(selected_objects) != 1:
        raise ValueError ('please select only one object')
    else:
        global sele_shape
        sele_shape = cmds.listRelatives(sele, shapes = True)
        if not cmds.objectType(sele_shape) == 'camera':
            raise ValueError("The selection should be a single camera")

# transferring the settings
def transfer_attr(source,child, inConnections ):
    if inConnections:
        cmds.copyAttr(source,child,values=True,inConnections=True)
    else:
        cmds.copyAttr(source,child,values=True)

# will toogle the Image sequence FrameExtension 
def image_sequence(new_image, status):
    cmds.setAttr ('%s.useFrameExtension'  %new_image, status)


# cheching for any curves inside the camera shape, this is mainly to get the focal curve incase if available. And pasting that in to the new camera. 
def copy_paste_keys(source, child):
    copy_keys = cmds.copyKey(source)
    if copy_keys:
        cmds.pasteKey(child)

# locking the attributes. 
def lock_attr(cam_attr, cam, grp):
    for attr in cam_attr:
        cmds.setAttr('%s.%s' % (cam, attr) , lock = True)
    for i in cam_attr[:3]:
        cmds.setAttr('%s.%s' % (grp, i) , lock = True)

# copying the selected camera image plane values including the sequence path and pasting that in to a newly created image plane which is connected to the new camera. 
# If no source image available then its directly move on to the bake process. 
def setup_image(sele):

    global source_image
    source_image = cmds.listRelatives(cmds.listRelatives(sele))
    if source_image:
        global  source_image_shape, source_image_path
        source_image_shape = cmds.listRelatives(source_image)
        source_image_path = cmds.getAttr('%s.imageName' %source_image[0])   

        global new_cam_image, new_cam_image_shape
        new_cam_image, new_cam_image_shape = cmds.imagePlane(camera = new_cam, fileName = source_image_path)
        transfer_attr( source_image_shape, new_cam_image_shape, inConnections = True)
        image_sequence(new_cam_image_shape, 0)


# this is the major function . Inside this we have combined all the other functions and codes to produce a baked camera. 
def cam_bake():

    # creating a fresh camera 
    global new_cam,new_cam_shape
    new_cam,new_cam_shape = cmds.camera(n = 'MM_camera')
    
    # parenting that camera with the selected camera  
    parent_newcam_node = cmds.parentConstraint(sele, new_cam, maintainOffset = False)

    setup_image(sele)

    # baking the new camera channels and deleting the constraint. 
    cmds.bakeResults( new_cam , time=(StartTime,EndTime) )
    cmds.delete(parent_newcam_node)
    
    if source_image:
        image_sequence(new_cam_image_shape, 1)

    transfer_attr( sele_shape,new_cam_shape, inConnections = False)

    copy_paste_keys(sele_shape, new_cam_shape )
    
    # creating a new group for the newly created camera. Add that under this group. 
    Render_camera_grp = cmds.group(n = 'RenderCamGroup', empty = True)
    cmds.parent(new_cam, Render_camera_grp)

    cam_attr = ['translate', 'rotate', 'scale', 'focalLength', 'horizontalFilmAperture', 'verticalFilmAperture' ]
    lock_attr(cam_attr, new_cam, Render_camera_grp)
    
    
validate_selection(sele)

cam_bake()










