import bpy
import os

class LoadTexturesOperator(bpy.types.Operator):
    bl_idname = "object.load_textures"
    bl_label = "Load Textures from Directory"
    
    directory_path: bpy.props.StringProperty(subtype='DIR_PATH')
    target_material_name: bpy.props.StringProperty(default="Material")
    node_name_to_connect: bpy.props.StringProperty(default="Diffuse BSDF")

    def execute(self, context):
        # Get the target material
        target_material = bpy.data.materials.get(self.target_material_name)
        if not target_material:
            self.report({'ERROR'}, f"Material '{self.target_material_name}' not found.")
            return {'CANCELLED'}
        
        # List all files in the specified directory
        file_list = [f for f in os.listdir(self.directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.exr'))]
        
        # Iterate over the files and add textures to the material
        for filename in file_list:
            texture = bpy.data.textures.new(name=filename, type='IMAGE')
            image_path = os.path.join(self.directory_path, filename)
            image = bpy.data.images.load(image_path)
            texture.image = image
            
            # Create a node and link it to the material
            shader_node = target_material.node_tree.nodes.new(type='ShaderNodeTexImage')
            shader_node.image = image
            shader_node.location = (0, 0)
            
            # Connect the image texture to the specified node
            if self.node_name_to_connect:
                output_node = target_material.node_tree.nodes.get(self.node_name_to_connect)
                if output_node:
                    target_material.node_tree.links.new(shader_node.outputs['Color'], output_node.inputs['Base Color'])
        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Register the operator
def register():
    bpy.utils.register_class(LoadTexturesOperator)

def unregister():
    bpy.utils.unregister_class(LoadTexturesOperator)

if __name__ == "__main__":
    register()
