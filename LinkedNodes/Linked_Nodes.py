import bpy
from vb30.plugins import PLUGINS_ID
from bpy.props import IntProperty, StringProperty

bpy.types.Scene.linkcount = IntProperty(default = 0)
bpy.types.Scene.nodename = StringProperty(default = '')
bpy.types.Scene.nodematerialname = StringProperty(default = '')

#bpy.context.scene['picknode'] = 0

################################################
def node_set():

	mat = bpy.context.object.active_material.name
	bpy.context.scene.nodename = bpy.data.node_groups[mat].nodes.active.name
	bpy.context.scene.nodematerialname = mat

################################################
def node_pick():

	mat = bpy.context.object.active_material
	bpy.context.scene.nodename = bpy.data.node_groups[mat.name].nodes.active.name
	bpy.context.scene.nodematerialname = mat.name

def bitmap_create_new_texture(node):
	# Create new texture, for bitmap
	tex = bpy.data.textures.new(node.texture.name, type = 'IMAGE')
	image = node.texture.image
	node.texture = tex
	node.texture.image = image

def node_unlink():

	mat = bpy.context.object.active_material
	nodes = bpy.data.node_groups[mat.name].nodes

	nodelist = [n for n in nodes if n.select == True]
	for node in nodelist:
		vrayplugins = vray_plugins_get(node)
		if  'BitmapBuffer' in vrayplugins:
			bitmap_create_new_texture(node)
			#print ("unlink Bitmapbuffer")

		node.label = ""
		node.use_custom_color = False


################################################

def node_label_change(act_node):

	if act_node.label == "":  #change label only if active node label is empty
		act_node.label = "|Link|" + str(bpy.context.scene.linkcount) + act_node.name
		bpy.context.scene.linkcount += 1

################################################

def node_label_search_all(act_node):

	#loop all nodes
	#input: (active node, var:act_node)
	node_list = []
	nodes = bpy.data.node_groups

	for nodegroup in nodes:
		for node in nodegroup.nodes:
			if node.label == act_node.label and node != act_node:
				#print ("Search all:", node.name)
				node_list.append(node)

	#input()
	#print ("nodelist :",node_list)
	#input()
	return node_list

################################################

def node_label_search(act_node):

	#loop all nodes
	#input: (active node, var:act_node)
	node_list = []
	nodes = bpy.data.node_groups

	for nodegroup in nodes:
		for node in nodegroup.nodes:
			if node.label == act_node.label and node.name != act_node.name:
				#print (node.name)
				node_list.append(node)

	return node_list

################################################

def vray_plugins_get(node):

	vray_plugins = []
	vray_plugins.append(node.vray_plugin)

	for i in dir(node):

		if i != "__dict__":
			#print ("Vray plugin",i)
			if i != node.vray_plugin:
				vray_plugins.append(i)
		else:
			break

	return vray_plugins

################################################

def sockets_copy(node_source,node_target):

	for i,input in enumerate(node_target.inputs):
		try:
			input.value = node_source.inputs[i].value
			#print ("inputs copied:",node_source.inputs[i].name,node_source.inputs[i].value)
		except AttributeError:
			input.values = node_source.inputs[i].values
			#print ("ERROR input socket",i)
	for i,output in enumerate(node_target.outputs):
		output.value = node_source.outputs[i].value
		#print ("inputs copied:",node_source.inputs[i].name,node_source.inputs[i].value)

################################################

def socket_find(inputs,string):

	socket_number = -1
	for i, v in enumerate(inputs):
		#print ("def socket input:",i,v.vray_attr, string)
		if v.vray_attr == string:
			#print()
			#print("Socket found", i,v)
			#print()
			socket_number = i
			break

	return socket_number

#############################################
def selected_nodes_from_one_material():

	selected = []
	mat = bpy.context.object.active_material.name
	nodes = bpy.data.node_groups[mat].nodes

	for i in nodes:
		if i.select == True:
			selected.append(i)

	return selected

################################################

def selected_nodes(act_node,nodes):

	selected = []
	for i in nodes:
		if i.select and i.name != act_node.name:
			#print (i.name)
			selected.append(i)

	return selected

################################################

def node_copy(copy_update_paste_pastelink):

	#0 = copy
	#1 = update
	#2 = paste data
	#3 = paste data + link

	mat = bpy.context.object.active_material
	act_node = bpy.data.node_groups[mat.name].nodes.active
	vrayplugins = vray_plugins_get(act_node)

	attributes = []

	#paste data, paste+link data (2,3)
	if copy_update_paste_pastelink in (2,3):
		act_node = bpy.data.node_groups[bpy.context.scene.nodematerialname].nodes[bpy.context.scene.nodename]
		sel_nodes = selected_nodes_from_one_material()
		#act_node.label = "|Link|" + str(bpy.context.scene.linkcount) + act_node.name
		#bpy.context.scene.linkcount += 1
		if copy_update_paste_pastelink == 3: #pastelink
			node_label_change(act_node)

	#Update
	elif copy_update_paste_pastelink == 1:

		if act_node.label != "":
			sel_nodes = node_label_search_all(act_node)
			#iterate all nodes

			#print ("all nodes:",set(sel_nodes))

		else:
			#print ("label is empty")
			return
	else:#Copy
		node_label_change(act_node)
		
		nodes = bpy.data.node_groups[mat.name].nodes
		sel_nodes = selected_nodes(act_node,nodes)
		#print ("sel_node.name:",sel_nodes)

	for vrayplugin in vrayplugins:

		pluginID = vrayplugin
		pluginDesc = PLUGINS_ID[pluginID]
		#print ("pluginDesc =", PLUGINS_ID[pluginID])

		propGroup = getattr(act_node, pluginID)
		#print ("propGroup =",propGroup )

		#print ("---------------------------")
		#print("Plugin: %s" % pluginID)
		#print ("---------------------------")
		#print(pluginDesc.PluginParams)

		for attrDesc in pluginDesc.PluginParams:
			attrName = attrDesc['attr']
			attrDefault = attrDesc['default']

			if attrDefault != None:
				#print ("Sending :",act_node.inputs,"attribute name:", attrName)
				socket_number = socket_find(act_node.inputs,attrName)
				if socket_number >= 0:
					#sel_node.inputs[i]
					#print()
					#print ("Socket input:",socket_number, attrName)
					pass

				else:
					socket_number = socket_find(act_node.outputs,attrName)
					if socket_number >= 0:
						#print()
						#print ("Socket output:",socket_number, attrName)
						pass
					else:
						#no sockets found
						#print ("no sockets found")
						pass

				for i,selected_node in enumerate(sel_nodes):

					sel_node = selected_node
					s0 = "get = act_node." + pluginID + "." + attrName
					s1 = "sel_node." + pluginID + "." + attrName +"= get"
					#print (i, "SEL NODES", s0, s1, "Default:", attrDefault)
					try:
						exec(s0)
						exec(s1)
					except AttributeError:
						#print ("AttributeError")
						pass
			else:
				#print ()
				#print ("None value found", attrName)
				#print ()
				#input()
				pass
			attributes.append(attrName)

	for selected_node in sel_nodes:
		#print ("copy_update_paste_pastelink:",copy_update_paste_pastelink)
		#input()
		#try to copy texture
		try:
			if copy_update_paste_pastelink in (0,1,3): #copy, update,paste data
				selected_node.label = act_node.label
				selected_node.use_custom_color = act_node.use_custom_color
				selected_node.color = act_node.color

			selected_node.texture = act_node.texture
			selected_node.mapping_type = act_node.mapping_type
			if copy_update_paste_pastelink == 2: #paste data
				vrayplugins = vray_plugins_get(selected_node)
				try:
					if 'BitmapBuffer' in vrayplugins:
						bitmap_create_new_texture(selected_node)

				except AttributeError:
					#print ("attributeerror")
					pass
		except AttributeError:
			#print ("attributeerror")
			pass
		#print ("copy active node to:",selected_node.name)
		sockets_copy(act_node,selected_node)

	return len(sel_nodes)

