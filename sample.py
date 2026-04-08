import bpy
import random

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

num_cubes = 50
for i in range(num_cubes):
    x = random.uniform(-2, 2)
    y = random.uniform(-2, 2)
    z = random.uniform(-2, 2)
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(x, y, z))
    cube = bpy.context.active_object

    frame = 1
    while frame <= 200:
        # Initial position
        bpy.context.scene.frame_set(frame)
        cube.keyframe_insert(data_path="location")

        # Exploded position
        dx = random.uniform(-10, 10)
        dy = random.uniform(-10, 10)
        dz = random.uniform(-10, 10)
        cube.location = (x + dx, y + dy, z + dz)

        frame += 20   # step forward
        bpy.context.scene.frame_set(frame)
        cube.keyframe_insert(data_path="location")
