import bpy

# Get objects from a specific collection (replace with your collection name if needed)
cubes = bpy.data.collections[0].objects  

offset = 0

for x in cubes:  # iterate through each cube
    # Start invisible
    x.scale = (0, 0, 0)
    x.keyframe_insert(data_path="scale", frame=1 + offset)

    # Grow tall
    x.scale = (1, 1, 5)
    x.keyframe_insert(data_path="scale", frame=50 + offset)

    # Hold tall
    x.scale = (1, 1, 5)
    x.keyframe_insert(data_path="scale", frame=70 + offset)

    # Return to normal cube
    x.scale = (1, 1, 1)
    x.keyframe_insert(data_path="scale", frame=80 + offset)

    # Add stagger so each cube animates slightly later
    offset += 5
