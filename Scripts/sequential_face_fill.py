import bpy
import math
import mathutils
import bmesh

bl_info = {
    "name": "Sequential Face Fill",
    "author": "Alex Handby",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sequential Face Fill",
    "description": "given a selected array of edges fills faces between them",
    "warning": "",
    "doc_url": "",
    "category": "Edge Editing",
}

class CenteredEdge:    
    def __init__(self, edge, center):
        self.edge = edge
        self.center = center

def get_selected_edges(bm):
    return [e for e in bm.edges if e.select]

def calculate_centroid(world_coords):
    centroid = mathutils.Vector()
    num_coords = len(world_coords)
    for coords in world_coords:
        centroid += coords
    if centroid.x != 0:
        centroid.x /= num_coords
    if centroid.y != 0:
        centroid.y /= num_coords
    if centroid.z != 0:
        centroid.z /= num_coords    
    return centroid

#no longer necessary with bmesh
#def get_edge_verts(edge):
#    verts = []
#    obj = bpy.context.active_object
#    verts.append(obj.data.vertices[edge.vertices[0]])
#    verts.append(obj.data.vertices[edge.vertices[1]])
#    return verts

def get_center_of_edge(edge):
    obj = bpy.context.active_object
    matrix_world = obj.matrix_world
    verts = edge.verts
    world_coords = [matrix_world @ v.co for v in verts]
    cen = calculate_centroid(world_coords)
    return cen

def get_centers_of_edges(edges):
    return [CenteredEdge(e, get_center_of_edge(e)) for e in edges]

def create_debug_ico_sphere(cen):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.01, enter_editmode=False, align='WORLD', location=cen, scale=(1, 1, 1))
    
def create_debug_ico_spheres(centered_edges):
    for centered_edge in centered_edges: create_debug_ico_sphere(centered_edge.center)

def find_closest_edge(cedge, cedges):
    closest_distance = 999999999999999999999
    closest_edge = None
    for ce in cedges:
        if ce == cedge: continue
        dist = math.dist(cedge.center, ce.center)
        if dist < closest_distance:
             closest_distance = dist
             closest_edge = ce
    return closest_edge

def find_furthest_edge(cedge, cedges):
    largest_distance = 0
    furthest_edge = cedge
    for ce in cedges:
        if ce == cedge: continue
        dist = math.dist(cedge.center, ce.center)
        if dist > largest_distance:
             longest_distance = dist
             furthest_edge = ce
    return furthest_edge
    
def deselect_all_edges(bm):
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.select_flush(True)

def walk_along_creating_faces(bm, start, cedges):
    deselect_all_edges(bm)
    closest_cedge = find_closest_edge(start, cedges)
    closest_cedge.edge.select = True
    start.edge.select = True
    bm.select_flush(True)
    bpy.ops.mesh.bridge_edge_loops()
    cedges.remove(start)
    if len(cedges) > 1:
        walk_along_creating_faces(bm, closest_cedge, cedges)
    
    
             
         

class SequentialFaceFill(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.sequential_face_fill"
    bl_label = "Sequential Face Fill"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None
        
        edges = get_selected_edges(bm)
        
        print(f'selected edges: {len(edges)}')
        
        if len(edges) == 0:
            print("no edges selected")
            return {'FINISHED'}
        
        cedges = get_centers_of_edges(edges)
        print(f'number of cedges: {len(cedges)}')
        
        start = find_furthest_edge(cedges[0], cedges)
        walk_along_creating_faces(bm, start, cedges)
        
        bmesh.update_edit_mesh(me, loop_triangles=True)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SequentialFaceFill.bl_idname, text=SequentialFaceFill.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(SequentialFaceFill)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)


def unregister():
    bpy.utils.unregister_class(SequentialFaceFill)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.sequential_face_fill()
