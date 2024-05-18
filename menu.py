import nuke
import BreakRenderPass,FlipHorizontalNodes,OrgaincAlphaFeather,TidyUpNodes


my_menu = nuke.menu('Nodes').addMenu('My_Nuke_Tools')
my_menu.addCommand("BreakRenderPass", 'BreakRenderPass.main()',icon='ListShuffle.png',shortcut='shift+s')
my_menu.addCommand("FlipHorizontalNodes", 'FlipHorizontalNodes.main()', icon='ListShuffle.png',shortcut='shift+f')
my_menu.addCommand("TidyUpNodes", 'TidyUpNodes.main()',icon='ListShuffle.png',shortcut='ctrl+f')
my_menu.addCommand("Orgainc Alpha Feather", 'OrgaincAlphaFeather.main()', icon='OrgaincAlphaFeather.png')
my_menu.addCommand( "ShotInfo", "nuke.createNode('Shot_info')")


from nukeserversocket import nukeserversocket
nukeserversocket.install_nuke()

import nuke_comfyui as comfyui
comfyui.setup()