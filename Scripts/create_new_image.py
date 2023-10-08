import bpy
import os

class CreateImageAndConnectToMaterialOperator(bpy.types.Operator):
    bl_idname = "image.create_and_connect"
    bl_label = "Create Image and Connect to Material"
    
    def execute(self, context):
        # Create a new image
        image_width = 512
        image_height = 512
        new_image = bpy.data.images.new(name="NewImage", width=image_width, height=image_height)
        
        # Save the image to a file
        image_filepath = os.path.join(bpy.app.tempdir, "new_image.png")
        new_image.save_render(image_filepath)
        
        # Create a new material or select an existing one
        material_name = "NewMaterial"
        if material_name in bpy.data.materials:
            material = bpy.data.materials[material_name]
        else:
            material = bpy.data.materials.new(name=material_name)
        
        # Create a shader node
        shader_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
        shader_node.location = (0, 0)
        shader_node.image = new_image
        
        # Link the shader node to the material output
        material_output = material.node_tree.nodes.get("Material Output")
        if material_output:
            material.node_tree.links.new(shader_node.outputs["Color"], material_output.inputs["Surface"])
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(CreateImageAndConnectToMaterialOperator.bl_idname)

def register():
    bpy.utils.register_class(CreateImageAndConnectToMaterialOperator)
    bpy.types.VIEW3D_MT_image.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CreateImageAndConnectToMaterialOperator)
    bpy.types.VIEW3D_MT_image.remove(menu_func)

if __name__ == "__main__":
    register()
