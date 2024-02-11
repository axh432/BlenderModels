import bpy

# Clear existing mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Specify the desired name for the Bezier curve
curve_name = "MyBezierCurve"
profile_name = "Circle"

# Create a Bezier circle
bpy.ops.curve.primitive_bezier_circle_add(radius=2, location=(0, 0, 0))
curve = bpy.context.object.data
bpy.context.object.name = curve_name  # Rename the curve object

# Create a circle mesh
bpy.ops.mesh.primitive_circle_add(radius=0.1, location=(0, 0, 0))
circle = bpy.context.object.data

# Create a Bezier circle profile
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = bpy.context.scene.objects[curve_name]
bpy.ops.object.duplicate(linked=False)
profile = bpy.context.object.data

# Create a new object for the extruded result
bpy.ops.object.select_all(action='DESELECT')
BezierCurve = bpy.context.scene.objects[curve_name]

BezierCurve.select_set(True)
bpy.context.view_layer.objects.active = BezierCurve  
bpy.ops.object.convert(target='MESH')
extrusion = bpy.context.object.data

# Create the modifier for extrusion along the curve
bpy.context.view_layer.objects.active = bpy.context.scene.objects[curve_name]
bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
bpy.context.object.modifiers["Array"].curve = bpy.data.objects[curve_name]
bpy.ops.object.modifier_add(type='CURVE')
bpy.context.object.modifiers["Curve"].object = bpy.data.objects[curve_name]

# Apply the modifiers to finalize the extrusion
bpy.ops.object.modifier_apply({"object": bpy.context.scene.objects[curve_name]}, modifier="Array")
bpy.ops.object.modifier_apply({"object": bpy.context.scene.objects[curve_name]}, modifier="Curve")

# Clean up unnecessary objects
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = bpy.context.scene.objects[curve_name]
bpy.context.view_layer.objects.active.select_set(True)
bpy.ops.object.delete()

# Select the resulting mesh for further adjustments
bpy.context.view_layer.objects.active = bpy.context.scene.objects[curve_name]
bpy.context.view_layer.objects.active.select_set(True)
