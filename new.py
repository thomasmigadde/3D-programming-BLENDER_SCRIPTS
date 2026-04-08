import bpy
import random
import mathutils

def create_explosion_animation():
    # 1. Clear scene safely
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # 2. Configuration
    num_cubes = 50
    explosion_duration = 60      # How long the explosion lasts (frames)
    stagger_max = 20             # Random delay before each cube explodes
    initial_bounds = (-2, 2)     # Starting area
    explosion_dist = (5, 12)     # How far they fly
    cube_size = 0.5

    # Set timeline range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = explosion_duration + stagger_max + 20

    for i in range(num_cubes):
        # Initial random position
        init_loc = mathutils.Vector((
            random.uniform(*initial_bounds),
            random.uniform(*initial_bounds),
            random.uniform(*initial_bounds)
        ))

        # Create cube (using ops is fine for ~50-100 objects)
        bpy.ops.mesh.primitive_cube_add(size=cube_size, location=init_loc)
        cube = bpy.context.active_object
        cube.name = f"ExploCube_{i}"

        # Random explosion direction (normalized vector)
        direction = mathutils.Vector((random.uniform(-1, 1) for _ in range(3)))
        if direction.length < 0.001:
            direction = mathutils.Vector((0, 0, 1))
        direction.normalize()

        # Random distance
        dist = random.uniform(*explosion_dist)
        final_loc = init_loc + direction * dist

        # Random stagger (start frame)
        start_frame = 1 + random.randint(0, stagger_max)
        end_frame = start_frame + explosion_duration

        # Keyframe Location
        cube.location = init_loc
        cube.keyframe_insert(data_path="location", frame=start_frame)
        cube.location = final_loc
        cube.keyframe_insert(data_path="location", frame=end_frame)

        # Keyframe Rotation (spin during flight)
        cube.rotation_euler = (0, 0, 0)
        cube.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        cube.rotation_euler = (random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-3, 3))
        cube.keyframe_insert(data_path="rotation_euler", frame=end_frame)

        # Set interpolation for explosive feel (QUAD_OUT starts fast, slows down)
        if cube.animation_data and cube.animation_data.action:
            for fcurve in cube.animation_data.action.fcurves:
                if fcurve.data_path in ("location", "rotation_euler"):
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'QUAD_OUT'

    bpy.context.scene.frame_current = 1
    print(f"✅ Created {num_cubes} exploding cubes. Timeline: {bpy.context.scene.frame_start}-{bpy.context.scene.frame_end}")

if __name__ == "__main__":
    create_explosion_animation()
    