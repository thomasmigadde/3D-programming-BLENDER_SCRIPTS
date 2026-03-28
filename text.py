import bpy

# Delete all existing objects (optional, to start fresh)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Cube size
cube_size = 1.0

# Dimensions of the cuboid (number of cubes along x, y, z)
nx, ny, nz = 20, 5, 1  # 20 * 5 * 1 = 100 cubes (one layer)

# Loop to create cubes
for i in range(nx):
    for j in range(ny):
        for k in range(nz):  # only one layer since nz=1
            bpy.ops.mesh.primitive_cube_add(
                size=cube_size,
                location=(i * cube_size,
                          j * cube_size,
                          k * cube_size)
            )
