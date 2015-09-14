# Vray-Linked-Nodes


Nodes: label based linked nodes

Supported nodes:
Material
BRDF
Textures
Mapping

Not working nodes:
BRDF Layered
Gradient ramp
Remap

-
Buttons:
-
Link
Link all selected nodes, active node is the source node

UnLink
UnLink all selected nodes

Copy Node Data
Copy active node values, nothing visual

Paste Node Data
Paste copied node values to selected nodes, no linking

Paste+Link Data
Paste copied node values to selected nodes + link them

Update Node
Updates nodes which are linked to active node

Paste Node Data and Paste+Link Data buttons are mainly to paste/link node values to another material nodes

-

You can also copy/paste (Ctrl+C, Ctrl+V) nodes between materials in normal way, if nodes are set to link, then pasted nodes are also linked.

Cons:
Uses node labels to link nodes so dont change them
Might crash Blender, no node type checks yet
