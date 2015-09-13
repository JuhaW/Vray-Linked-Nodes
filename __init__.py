bl_info = {
    "name": "Vray Linked nodes",
    "description": " Label based linked nodes for Vray",
    "author": "Juha W",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Node Editor > Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}


import bpy
import sys
import os.path
import importlib

sys.path.append('C:\Vray addons\VrayLinkedNodes')
os.path.join('C:\Vray addons\VrayLinkedNodes')

from LinkedNodes import Linked_Nodes as f
importlib.reload(f)

#from ReloadScript import Reload_Script as r

###########################################################

class ShowLinked(bpy.types.Panel):

	bl_label = "Nodes"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "TOOLS"
	bl_category = "Trees"

	def draw(self, context):

		scene = context.scene
		layout = self.layout
		row = layout.row()

		row.operator('nodes.copy', text ='Link')

		row = layout.row()
		row.operator('nodes.unlink', text ='UnLink')
		row = layout.row()
		#row.label(str(scene.linkcount))
		#row = layout.row()
		row.operator('node.copydata', text ='Copy Node Data')
		row = layout.row()
		row.operator('node.pastedata', text ='Paste Node Data')
		row = layout.row()
		row.operator('node.pastelink', text ='Paste+Link Data')
		row = layout.row()
		row.label(scene.nodename)
		row = layout.row()
		row.label(scene.nodematerialname)
		row = layout.row()
		row.operator('nodes.update', text ='Update Node')
		#row.operator('script.unregister', text ='Unregister')
		#row.operator('script.reload_my_scripts')

###########################################################

class Nnodes_pastelink(bpy.types.Operator):
	bl_idname = 'node.pastelink'
	bl_label = 'Paste+Link Data'

	def execute(self,context):

		#cnt = f.node_copy(True)
		f.node_copy(3)
		#self.report({'INFO'},str(cnt + 1) + "Node linked")
		return {'FINISHED'}

###########################################################

class Nnodes_pastedata(bpy.types.Operator):
	bl_idname = 'node.pastedata'
	bl_label = 'Paste Node Data'

	def execute(self,context):

		#cnt = f.node_copy(True)
		f.node_copy(2)
		#self.report({'INFO'},str(cnt + 1) + "Node linked")
		return {'FINISHED'}

###########################################################

class Nnodes_pickdata(bpy.types.Operator):
	bl_idname = 'node.copydata'
	bl_label = 'Copy Node Data'

	def execute(self,context):

		#cnt = f.node_copy(True)
		f.node_pick()
		#self.report({'INFO'},str(cnt + 1) + "Node linked")
		return {'FINISHED'}

#################################################################


class Nnodes_copy(bpy.types.Operator):
	bl_idname = 'nodes.copy'
	bl_label = 'Set link'

	#update aina aktiivisen noden mukaiseksi muut linkatut

	def execute(self,context):

		cnt = f.node_copy(0)
		self.report({'INFO'},str(cnt + 1) + "Nodes linked")

		return {'FINISHED'}

#################################################################

class Nnodes_update(bpy.types.Operator):
	bl_idname = 'nodes.update'
	bl_label = 'Update link'

	#update aina aktiivisen noden mukaiseksi muut linkatut

	def execute(self,context):

		cnt = f.node_copy(1)
		self.report({'INFO'},str(cnt) + "Nodes updated")
		return {'FINISHED'}

#################################################################

class Nnodes_unlink(bpy.types.Operator):
	bl_idname = 'nodes.unlink'
	bl_label = 'Unlink'

	#update aina aktiivisen noden mukaiseksi muut linkatut

	def execute(self,context):

		f.node_unlink()

		return {'FINISHED'}

#################################################################



class Unregister(bpy.types.Operator):
	bl_idname = 'script.unregister'
	bl_label = 'Unregister'

	def execute(self,context):

		unregister()

		return {'FINISHED'}

#################################################################

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()

