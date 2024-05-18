import nuke

def flipHNodes(node_list):
    num = len(node_list)
    center_x = sum([n.xpos()+n.screenWidth()/2.0 for n in node_list])/num
    for n in node_list:
        x = n.xpos()
        offset = center_x - (x+n.screenWidth()/2.0)
        n['xpos'].setValue(x+2*offset)

def main():
    nodes = nuke.selectedNodes()
    if len(nodes)>0:
        flipHNodes(nodes)

# main()

