import os
import nuke

icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'icons'))
gizmos_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'gizmos'))

nuke.pluginAddPath(icon_path,addToSysPath=False)
nuke.pluginAddPath(gizmos_path,addToSysPath=False)

version = nuke.env['NukeVersionMajor']

def main():
	for selectedNode in nuke.selectedNodes():
		node = nuke.createNode('OrgaincAlphaFeather_v11')
		node['blur_size'].setValue(30)
		node['displace_scale'].setValue(30)
		node['noise_size'].setValue(350)
		node['gain'].setValue(0.5)
		node['gamma'].setValue(0.5)    

