# extend Python's math functionality
import math

# give Python access to Blender's functionality
import bpy

# create cube
bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object

# create a list of locations for the empties
empty_locations = [
    (0, 0, 0),
    (0, 0, cube.dimensions.z), 
    (0, -cube.dimensions.y, cube.dimensions.z), 
    (0, -cube.dimensions.y, 0)]

# create variables for the rotation animation
rotation_animation_length = 15
current_frame = 1
rotation_angle = -90

# create a variable to track the previous empty (used for parenting)
previous_empty = None

# create a variable to set the number of times the cube will revolve
number_of_revolutions = 2

for _ in range(number_of_revolutions):
    # loop over all the empty locations
    for loc in empty_locations:
        # create an empty and update the location
        bpy.ops.object.empty_add()
        empty = bpy.context.active_object
        empty.location = loc
        
        # parent the empty to the previous empty
        if previous_empty:
            empty.parent = previous_empty
            # keep the transform when parenting
            empty.matrix_parent_inverse = previous_empty.matrix_world.inverted()
            
            # This is an alternative way to set a parent object and keep the transform            
            # previous_empty.select_set(True)
            # bpy.context.view_layer.objects.active = previous_empty
            # bpy.ops.object.parent_set(keep_transform=True)
        else:
            # save the root empty
            root_empty = empty
        
        previous_empty = empty
        
        # animate the rotation
        # insert first keyframe
        empty.keyframe_insert("rotation_euler", frame=current_frame)

        # rotate cube
        empty.rotation_euler.x = math.radians(rotation_angle)

        current_frame += rotation_animation_length
        # insert last keyframe
        empty.keyframe_insert("rotation_euler", frame=current_frame)
        
        # reset the rotation to not mess up the transform when parenting
        empty.rotation_euler.x = 0

# parent the cube to the last empty
cube.parent = previous_empty

# move cube into position
cube.location.x = cube.dimensions.x / 2
cube.location.y = cube.dimensions.y / 2
cube.location.z = cube.dimensions.z / 2

# update the location the cube roll
# root_empty.location.x = 10