import bpy
import random
import math

def create_boxes():
    boxes = []
    for _ in range(100):
        loc = (random.randrange(0, 20, 2),
               random.randrange(0, 20, 2),
               random.randrange(0, 20, 2))
        bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
        boxes.append(bpy.context.active_object)
    return boxes

def get_boxes_in_radius(boxes, center, radius):
    # math.dist is available in Python 3.8+ and cleaner
    return [box for box in boxes if math.dist(box.location, center) <= radius]

def animate_explosion(boxes, target_frame=51):
    filtered = get_boxes_in_radius(boxes, center=(5.0, 5.0, 0.0), radius=3.0)
    if not filtered:
        print("No boxes within radius.")
        return
    
    # Safely pick up to 10 boxes
    num_to_pick = min(10, len(filtered))
    selected = random.sample(filtered, num_to_pick)
    
    for obj in selected:
        # Frame 1: Initial state
        obj.keyframe_insert(data_path="location", frame=1)
        obj.keyframe_insert(data_path="rotation_euler", frame=1)
        obj.keyframe_insert(data_path="scale", frame=1)
        
        # Frame 51: Exploded state
        # Move outward from center + random offset
        direction = (obj.location - mathutils.Vector((5.0, 5.0, 0.0))).normalized()
        explosion_offset = direction * random.uniform(3.0, 6.0)
        obj.location += explosion_offset
        
        # Random rotation
        obj.rotation_euler = (
            math.radians(random.uniform(0, 360)),
            math.radians(random.uniform(0, 360)),
            math.radians(random.uniform(0, 360))
        )
        
        # Insert keyframes at target frame
        obj.keyframe_insert(data_path="location", frame=target_frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=target_frame)
        obj.keyframe_insert(data_path="scale", frame=target_frame)

def main():
    boxes = create_boxes()
    animate_explosion(boxes, target_frame=50)
    print("Animation setup complete.")

# Note: mathutils is needed for Vector operations
import mathutils
main()