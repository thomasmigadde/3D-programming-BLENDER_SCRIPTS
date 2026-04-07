# extend Python's math functionality
import math

# give Python access to Blender's functionality
import bpy

def create_cube():
    """Add a cube into the scene"""
    bpy.ops.mesh.primitive_cube_add()
    return bpy.context.active_object
    

def create_empty(location):
    # create an empty and update the location
    bpy.ops.object.empty_add()
    empty = bpy.context.active_object
    empty.location = location
    return empty


def parent(child_obj, parent_obj, keep_transform=False):
    """Parent the child object to the parent object"""
    child_obj.parent = parent_obj
    if keep_transform:
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()


def animate_rotation(obj, current_frame, rotation_angle, rotation_animation_length):
    """Animate the rotation of an object"""
    # insert first keyframe
    obj.keyframe_insert("rotation_euler", frame=current_frame)

    # rotate cube
    obj.rotation_euler.x = math.radians(rotation_angle)

    current_frame += rotation_animation_length
    # insert last keyframe
    obj.keyframe_insert("rotation_euler", frame=current_frame)

    # reset the rotation to not mess up the transform when parenting
    obj.rotation_euler.x = 0
    
    return current_frame


def animate_revolutions(number_of_revolutions, empty_locations, rotation_angle, rotation_animation_length):
    """Animate the roll of an object"""
    # create a variable to track the previous empty (used for parenting)
    previous_empty = None
    
    # create a variable to track the first empty (used for parenting)
    root_empty = None
    
    # create a variable to track the current_frame
    current_frame = 1
    
    for _ in range(number_of_revolutions):
        # loop over all the empty locations
        for loc in empty_locations:
            empty = create_empty(loc)

            # parent the empty to the previous empty
            if previous_empty:
                parent(empty, previous_empty, keep_transform=True)
            else:
                # save the root empty
                root_empty = empty

            previous_empty = empty

            current_frame = animate_rotation(empty, current_frame, rotation_angle, rotation_animation_length)
    
    # update the animation length
    bpy.context.scene.frame_end = current_frame
    
    return root_empty, previous_empty


def roll_cube(cube, number_of_revolutions, starting_position):
    """Create an animation of a rolling cube"""
    # create a list of locations for the empties
    empty_locations = [(0, 0, 0), (0, 0, cube.dimensions.z), (0, -cube.dimensions.y, cube.dimensions.z), (0, -cube.dimensions.y, 0)]

    # create variables for the rotation animation
    rotation_animation_length = 15
    rotation_angle = -90

    root_empty, previous_empty = animate_revolutions(number_of_revolutions, empty_locations, rotation_angle, rotation_animation_length)

    # parent the cube to the last empty
    cube.parent = previous_empty

    # move cube into position
    cube.location.x = cube.dimensions.x / 2
    cube.location.y = cube.dimensions.y / 2
    cube.location.z = cube.dimensions.z / 2

    # update the location the cube roll
    root_empty.location = starting_position


def main():
    cube = create_cube()

    # create a variable to set the number of times the cube will revolve
    number_of_revolutions = 2
    
    # create a variable to set the starting location of the roll animation
    starting_position = (5, 5, 0)

    roll_cube(cube, number_of_revolutions, starting_position)


main()