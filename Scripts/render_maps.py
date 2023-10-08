import bpy
import os

# Define the list of materials
materials = ["Material1", "Material2", "Material3", "Material4"]

# Operator to perform the texture baking and saving
class BakingOperator(bpy.types.Operator):
    bl_idname = "object.bake_texture_operator"
    bl_label = "Bake Textures"
    
    def execute(self, context):
        # Prompt the user to specify the output directory
        output_directory = bpy.path.abspath(input("Enter the output directory: "))
        
        # Create subdirectories for collections, sub-collections, and objects
        def create_subdirectories(obj, output_dir):
            if obj.type == 'MESH':
                collection_name = obj.users_collection[0].name
                subcollection_name = obj.users_collection[0].children[0].name if obj.users_collection[0].children else ""
                object_name = obj.name
                subdirectory = os.path.join(output_dir, collection_name, subcollection_name, object_name)
                os.makedirs(subdirectory, exist_ok=True)
                return subdirectory
            return None

        # Initialize progress variables
        total_steps = len(context.selected_objects) * len(materials)
        current_step = 0
        
        # Create a progress bar
        progress_bar = context.window_manager.progress_begin(0, total_steps)
        
        # Iterate through selected objects
        for obj in context.selected_objects:
            # Iterate through the list of materials
            for material_name in materials:
                # Assign the material to the object
                material = bpy.data.materials.get(material_name)
                if material is not None:
                    obj.data.materials.append(material)
                    
                    # Create a new texture
                    texture = bpy.data.textures.new(name="Texture", type='IMAGE')
                    texture.image = bpy.data.images.new(name="TextureImage", width=1024, height=1024)  # Adjust dimensions as needed
                    
                    # Assign the texture to the material
                    material.use_nodes = True
                    material.node_tree.links.new(material.node_tree.nodes['Principled BSDF'].inputs['Base Color'], material.node_tree.nodes['Image Texture'].outputs['Color'])
                    
                    # Set the texture's output path
                    subdirectory = create_subdirectories(obj, output_directory)
                    if subdirectory:
                        texture.image.file_format = 'PNG'  # Adjust format as needed
                        texture.image.filepath_raw = os.path.join(subdirectory, f"{material_name}.png")
                        
                        # Bake the texture
                        context.scene.render.bake(type='DIFFUSE', use_selected_to_active=True)
                        bpy.ops.object.bake(type='DIFFUSE')
                        
                        # Save the texture image
                        texture.image.save()
                        
                        # Clear the texture slot
                        material.node_tree.nodes['Image Texture'].image = None
                        
                        # Update progress
                        current_step += 1
                        context.window_manager.progress_update(progress_bar, current_step)
        
        # Clean up unused materials
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)
        
        # End the progress bar
        context.window_manager.progress_end()
        
        print("Texture baking and saving completed.")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(BakingOperator)

def unregister():
    bpy.utils.unregister_class(BakingOperator)

if __name__ == "__main__":
    register()
