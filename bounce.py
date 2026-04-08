import bpy

# Create two cubes
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
cube1 = bpy.context.active_object
bpy.ops.mesh.primitive_cube_add(location=(4,0,0))
cube2 = bpy.context.active_object

# Add rigid body physics
for obj in [cube1, cube2]:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = 'ACTIVE'   # Both can move
    obj.rigid_body.collision_shape = 'BOX'
    obj.rigid_body.restitution = 0.8 # Bounciness (0 = no bounce, 1 = very bouncy)

# Optional: give cube1 some initial velocity
cube1.rigid_body.linear_velocity = (5, 0, 0)
