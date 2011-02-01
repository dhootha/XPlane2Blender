import bpy
from io_xplane2blender.xplane_ops import *
from io_xplane2blender.xplane_config import *

class LAMP_PT_xplane(bpy.types.Panel):
    '''XPlane Material Panel'''
    bl_label = "XPlane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    def draw(self,context):
        obj = context.object

        if(obj.type == "LAMP"):
            lamp_layout(self,obj.data)
            custom_layout(self,obj.data,"LAMP")
    

class MATERIAL_PT_xplane(bpy.types.Panel):
    '''XPlane Material Panel'''
    bl_label = "XPlane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self,context):
        obj = context.object

        if(obj.type == "MESH"):
            material_layout(self,obj.active_material)
            custom_layout(self,obj.active_material,"MATERIAL")
    
class SCENE_PT_xplane(bpy.types.Panel):
    '''XPlane Scene Panel'''
    bl_label = "XPlane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    @classmethod
    def poll(self,context):
        return True

    def draw(self,context):
        scene = context.scene
        scene_layout(self, scene)

class OBJECT_PT_xplane(bpy.types.Panel):
    '''XPlane Object Panel'''
    bl_label = "XPlane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        obj = context.object

        if obj.type in ("MESH","EMPTY","ARMATURE"):
            return True
        else:
            return False

    def draw(self, context):
        obj = context.object
        
        if obj.type in ("MESH","EMPTY","ARMATURE"):
            mesh_layout(self,obj)
            animation_layout(self,obj)
            if obj.type == "MESH":
                cockpit_layout(self,obj)
                manipulator_layout(self,obj)
                custom_layout(self,obj,obj.type)

class BONE_PT_xplane(bpy.types.Panel):
    '''XPlane Object Panel'''
    bl_label = "XPlane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"

    @classmethod
    def poll(self,context):
        bone = context.bone

        if bone:
            return True
        else:
            return False

    def draw(self, context):
        bone = context.bone
        if bone:
            animation_layout(self,bone,True)

class OBJECT_MT_xplane_datarefs(bpy.types.Menu):
    '''XPlane Datarefs Search Menu'''
    bl_label = "XPlane Datarefs"

    def draw(self,context):
        self.search_menu(xplane_datarefs,"text.open")

def scene_layout(self, scene):
    layout = self.layout
    row = layout.row()

    for i in range(0,len(scene.layers)):
        row = layout.row()
        layer_layout(self, scene, row, i)
        

def layer_layout(self, scene, layout, layer):
    box = layout.box()
    li = str(layer+1)

    if scene.xplane.layers[layer].expanded:
        expandIcon = "TRIA_DOWN"
        expanded = True
    else:
        expandIcon = "TRIA_RIGHT"
        expanded = False

    box.prop(scene.xplane.layers[layer],"expanded", text="Layer "+li, expand=True, emboss=False, icon=expandIcon)

    if expanded:
        column = box.column()
        column.prop(scene.xplane.layers[layer],"name", text="Name")
        
        if scene.xplane.layers[layer].cockpit:
            checkboxIcon = "CHECKBOX_HLT"
        else:
            checkboxIcon = "CHECKBOX_DEHLT"

        column.label('Textures')
        tex_box = column.box()
        tex_box.prop(scene.xplane.layers[layer], "texture", text="Default")
        tex_box.prop(scene.xplane.layers[layer], "texture_lit", text="Night")
        tex_box.prop(scene.xplane.layers[layer], "texture_normal", text="Normal / Specular")
        column.prop(scene.xplane.layers[layer], "cockpit", text="Cockpit",icon=checkboxIcon, toggle=True)
        column.prop(scene.xplane.layers[layer], "slungLoadWeight", text="Slung Load weight")

        custom_layer_layout(self, box, scene, layer)

def custom_layer_layout(self,layout, scene, layer):
    layout.separator()
    row = layout.row()
    row.label("Custom Properties")
    row.operator("scene.add_xplane_layer_attribute", text="Add Property").index = layer
    box = layout.box()
    for i, attr in enumerate(scene.xplane.layers[layer].customAttributes):
        subbox = box.box()
        subrow = subbox.row()
        subrow.prop(attr,"name")
        subrow.prop(attr,"value")
        subrow.operator("scene.remove_xplane_layer_attribute",text="",emboss=False,icon="X").index = (layer,i)
        if type in ("MATERIAL","MESH"):
            subrow = subbox.row()
            subrow.prop(attr,"reset")
    

def mesh_layout(self, obj):
    layout = self.layout
    row = layout.row()
    row.prop(obj.xplane, "depth", text="Use depth culling")

def lamp_layout(self, obj):
    layout = self.layout
    row = layout.row()
    row.prop(obj.xplane, "lightType", text="Light type")

def material_layout(self, obj):
    layout = self.layout

    row = layout.row()
    row.prop(obj.xplane, "surfaceType", text="Surface type")

    row = layout.row()
    row.prop(obj.xplane, "blend", text="Use alpha cutoff")

    if(obj.xplane.blend==True):
        row = layout.row()
        row.prop(obj.xplane, "blendRatio", text="Alpha cutoff ratio")


def custom_layout(self,obj,type):
    if type in ("MESH"):
        oType = 'object'
    elif type=="MATERIAL":
        oType = 'material'
    elif type=='LAMP':
        oType = 'lamp'

    layout = self.layout
    layout.separator()
    row = layout.row()
    row.label("Custom Properties")
    row.operator("object.add_xplane_"+oType+"_attribute", text="Add Property")
    box = layout.box()
    for i, attr in enumerate(obj.xplane.customAttributes):
        subbox = box.box()
        subrow = subbox.row()
        subrow.prop(attr,"name")
        subrow.prop(attr,"value")
        subrow.operator("object.remove_xplane_"+oType+"_attribute",text="",emboss=False,icon="X").index = i
        if type in ("MATERIAL","MESH"):
            subrow = subbox.row()
            subrow.prop(attr,"reset")
    

def animation_layout(self,obj,bone = False):
    layout = self.layout
    layout.separator()
    row = layout.row()
    row.label("Datarefs")
    if bone:
        row.operator("bone.add_xplane_dataref", text="Add Dataref")
    else:
        row.operator("object.add_xplane_dataref", text="Add Dataref")
    box = layout.box()
    for i, attr in enumerate(obj.xplane.datarefs):
        subbox = box.box()
        subrow = subbox.row()
        # TODO: search is causing memory leak!
#        if len(bpy.data.scenes[0].xplane_datarefs)>0:
#            subrow.prop_search(attr,"path",bpy.data.scenes[0],"xplane_datarefs",text="",icon="VIEWZOOM")
#        else:
#            subrow.prop(attr,"path")
        subrow.prop(attr,"path")
        if bone:
            subrow.operator("bone.remove_xplane_dataref",text="",emboss=False,icon="X").index = i
        else:
            subrow.operator("object.remove_xplane_dataref",text="",emboss=False,icon="X").index = i
            
        subrow = subbox.row()
        subrow.prop(attr,"loop",text="Loops")
        subrow = subbox.row()

        if bone:
            subrow.operator("bone.add_xplane_dataref_keyframe",text="",icon="KEY_HLT").index = i
            subrow.operator("bone.remove_xplane_dataref_keyframe",text="",icon="KEY_DEHLT").index = i
        else:
            subrow.operator("object.add_xplane_dataref_keyframe",text="",icon="KEY_HLT").index = i
            subrow.operator("object.remove_xplane_dataref_keyframe",text="",icon="KEY_DEHLT").index = i
        subrow.prop(attr,"value")

def cockpit_layout(self,obj):
    layout = self.layout
    layout.separator()
    row = layout.row()
    row.prop(obj.xplane,'panel',text='Part of Cockpit panel')

def manipulator_layout(self,obj):
    layout = self.layout
    layout.separator()
    row = layout.row()
    row.prop(obj.xplane.manip,'enabled',text='Manipulator')

    if obj.xplane.manip.enabled:
        box = layout.box()
        box.prop(obj.xplane.manip,'type',text="Type")

        type = obj.xplane.manip.type
        
        box.prop(obj.xplane.manip,'cursor',text="Cursor")
        box.prop(obj.xplane.manip,'tooltip',text="Tooltip")

        if type!='drag_xy':
            box.prop(obj.xplane.manip,'dataref1',text="Dataref")
        else:
            box.prop(obj.xplane.manip,'dataref1',text="Dataref 1")
            box.prop(obj.xplane.manip,'dataref2',text="Dataref 2")

        # drag axis lenghts
        if type in ('drag_xy','drag_axis','command_axis'):
            box.prop(obj.xplane.manip,'dx',text="dx")
            box.prop(obj.xplane.manip,'dy',text="dy")
            if type in('drag_axis','command_axis'):
                box.prop(obj.xplane.manip,'dz',text="dz")

        # values
        if type=='drag_xy':
            box.prop(obj.xplane.manip,'v1_min',text="v1 min")
            box.prop(obj.xplane.manip,'v1_max',text="v1 max")
            box.prop(obj.xplane.manip,'v2_min',text="v2 min")
            box.prop(obj.xplane.manip,'v2_max',text="v2 max")
        elif type=='drag_axis':
            box.prop(obj.xplane.manip,'v1',text="v1")
            box.prop(obj.xplane.manip,'v2',text="v2")
        elif type=='command':
            box.prop(obj.xplane.manip,'command',text="Command")
        elif type=='command_axis':
            box.prop(obj.xplane.manip,'positive_command',text="Pos. command")
            box.prop(obj.xplane.manip,'negative_command',text="Neg. command")
        elif type=='push':
            box.prop(obj.xplane.manip,'v_down',text="v down")
            box.prop(obj.xplane.manip,'v_up',text="v up")
        elif type=='radio':
            box.prop(obj.xplane.manip,'v_down',text="v down")
        elif type=='toggle':
            box.prop(obj.xplane.manip,'v_on',text="v On")
            box.prop(obj.xplane.manip,'v_off',text="v Off")
        elif type in ('delta','wrap'):
            box.prop(obj.xplane.manip,'v_down',text="v down")
            box.prop(obj.xplane.manip,'v_hold',text="v hold")
            box.prop(obj.xplane.manip,'v1_min',text="v min")
            box.prop(obj.xplane.manip,'v1_max',text="v max")

def parseDatarefs():
    import os
    search_data = []
    filePath = os.path.dirname(__file__)+'/DataRefs.txt'
    if os.path.exists(filePath):
        try:
            file = open(filePath,'r')
            i = 0
            for line in file:
                if i>1:
                    parts = line.split('\t')
                    if (len(parts)>1 and parts[1] in ('float','int')):
                        search_data.append(parts[0])
                i+=1
        except IOError:
            print(IOError)
        finally:
            file.close()
    return search_data

def showError(message):
    wm = byp.context.window_manager
    wm.invoke_popup(bpy.ops.xplane_error)
    return {'CANCELLED'}

def showProgress(percent,message):
    wm = byp.context.window_manager
    wm.invoke_popup(bpy.ops.xplane_progress)
    return {'RUNNING_MODAL'}

def addXPlaneUI():
#    datarefs = parseDatarefs()
#
#    for dataref in datarefs:
#        prop = bpy.data.scenes[0].xplane_datarefs.add()
#        prop.name = dataref
    pass

def removeXPlaneUI():
    pass