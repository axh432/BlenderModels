bl_info = {
    "name": "Create Directories",
    "author": "Alex Handby",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy

class CreateDirectories(bpy.types.Operator):
    bl_idname = "object.create_directories"
    bl_label = "Create Directories"
    bl_description = "given a selected object create a series of directories that mirror it's location within collections"

    def execute(self, context):
        print("operator executed")
        return {'FINISHED'}

class CreateDirectoriesPanel(bpy.types.Panel):
    bl_label = "Create Directories Panel"
    bl_idname = "OBJECT_PT_CreateDirectoriesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_directories")

def register():
    bpy.utils.register_class(CreateDirectories)
    bpy.utils.register_class(CreateDirectoriesPanel)

def unregister():
    bpy.utils.unregister_class(CreateDirectories)
    bpy.utils.unregister_class(CreateDirectoriesPanel)

if __name__ == "__main__":
    register()

