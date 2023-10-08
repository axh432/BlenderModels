bl_info = {
    "name": "Copy Material Nodes",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_CopyMaterialNodes(bpy.types.Operator):
    bl_idname = "object.copy_material_nodes"
    bl_label = "Copy Material Nodes"
    bl_description = "Create new materials and copy nodes from a master material to selected objects"
    
    master_material_name: bpy.props.StringProperty(
        name="Master Material",
        description="Name of the master material to copy nodes from",
        default="Master Material"
    )
    
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Name of the collection containing objects",
        default="Your Collection Name"
    )

    def execute(self, context):
        # Get the collection
        collection = bpy.data.collections.get(self.collection_name)

        if collection is not None:
            # Iterate through selected objects in the collection
            for obj in collection.objects:
                if obj.select_get():
                    # Create a new material for each selected object
                    new_material = bpy.data.materials.new(name=f"{obj.name}_Material")

                    # Link the new material to the object
                    if obj.data.materials:
                        obj.data.materials[0] = new_material
                    else:
                        obj.data.materials.append(new_material)

                    # Get the master material
                    master_material = bpy.data.materials.get(self.master_material_name)

                    if master_material is not None:
                        # Copy the nodes from the master material to the new material
                        new_material.node_tree = master_material.node_tree.copy()
                    else:
                        self.report({'ERROR'}, f"Master material '{self.master_material_name}' not found!")

        else:
            self.report({'ERROR'}, f"Collection '{self.collection_name}' not found!")

        return {'FINISHED'}

class MATERIAL_PT_CopyMaterialNodesPanel(bpy.types.Panel):
    bl_label = "Copy Material Nodes"
    bl_idname = "MATERIAL_PT_CopyMaterialNodesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "master_material_name")
        layout.prop(context.scene, "collection_name")
        layout.operator("object.copy_material_nodes")

def register():
    bpy.utils.register_class(OBJECT_OT_CopyMaterialNodes)
    bpy.utils.register_class(MATERIAL_PT_CopyMaterialNodesPanel)
    bpy.types.Scene.master_material_name = bpy.props.StringProperty()
    bpy.types.Scene.collection_name = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CopyMaterialNodes)
    bpy.utils.unregister_class(MATERIAL_PT_CopyMaterialNodesPanel)
    del bpy.types.Scene.master_material_name
    del bpy.types.Scene.collection_name

if __name__ == "__main__":
    register()
