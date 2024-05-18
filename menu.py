import nuke
import BreakRenderPass
import FlipHorizontalNodes
import OrgaincAlphaFeather
import nuke_comfyui as comfyui

from nukeserversocket import nukeserversocket


my_menu = nuke.menu('Nodes').addMenu('My_Nuke_Tools')
my_menu.addCommand("BreakRenderPass", 'BreakRenderPass.main()', "",icon='ListShuffle.png')
my_menu.addCommand("FlipHorizontalNodes", 'FlipHorizontalNodes.main()', "",icon='ListShuffle.png')
my_menu.addCommand("Orgainc Alpha Feather", 'OrgaincAlphaFeather.main()', "",icon='OrgaincAlphaFeather.png')
my_menu.addCommand( "ShotInfo", "nuke.createNode('Shot_info')")

nukeserversocket.install_nuke()


comfyui.setup()