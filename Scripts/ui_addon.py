bl_info = {
    "name": "My Blender Addon",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class MyAddonPanel(bpy.types.Panel):
    bl_label = "My Addon Panel"
    bl_idname = "PT_MyAddonPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Checkbox
        layout.prop(context.scene, "my_checkbox_property", text="Enable Feature")

        # Dropdown menu
        layout.label(text="Select an option:")
        layout.prop(context.scene, "my_enum_property", text="")

        # Collection tree
        layout.label(text="Select a collection:")
        layout.prop_search(context.scene, "my_collection_property", context.scene, "collection", text="")

def register():
    bpy.utils.register_class(MyAddonPanel)
    bpy.types.Scene.my_checkbox_property = bpy.props.BoolProperty(name="Enable Feature")
    bpy.types.Scene.my_enum_property = bpy.props.EnumProperty(
        name="Dropdown Menu",
        items=[
            ("OPTION1", "Option 1", "Description for Option 1"),
            ("OPTION2", "Option 2", "Description for Option 2"),
        ]
    )
    bpy.types.Scene.my_collection_property = bpy.props.StringProperty(name="Collection")

def unregister():
    bpy.utils.unregister_class(MyAddonPanel)
    del bpy.types.Scene.my_checkbox_property
    del bpy.types.Scene.my_enum_property
    del bpy.types.Scene.my_collection_property

if __name__ == "__main__":
    register()

