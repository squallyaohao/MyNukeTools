import nuke

def tidyUpNodes(node):
    all_nodes = [node]
    inputs = getInputNodes(node)
    outputs = getOutputNodes(node)
    x = node.xpos()
    y = node.ypos()
    w = node.screenWidth()
    y = node.screeHeight()
    for i,n in inputs:
        _x = n.xpos()
        _y = n.ypos()
        _w = n.screenWidth()
        _h = n.screeHeight()
        if n.Class() != 'Dot':
            if abs(_x-x)>0.5*(w+_w) and (abs(_y-y)>0.5*(_h+h)):
                dot = nuke.nodes.Dot()
                dot['xpos'].setValue(x+0.5*w-6)
                dot['ypos'].setValue(_y+0.5*_h-6)
                dot.setInput(0,n)
                node.setInput(i,dot)
                all_nodes.append([dot,n])
            elif abs(_x - x)<0.5*(w+_w):
                n['xpos'].setValue(x)
                all_nodes.append(n)
            else:
                n['ypos'].setValue(y)
                all_nodes.append(n)
    
    for i,n in outputs:
        nuke.autoplaceSnap(n)
        _x = n.xpos()
        _y = n.ypos()
        _w = n.screenWidth()
        _h = n.screenHeight()
        if n.Class() != 'Dot':
            if abs(_x - x)>0.5*(w+_w) and (abs(_y-y)>0.5*(_h+h)):
                dot = nuke.nodes.Dot()
                dot['xpos'].setValue(_x + 0.5 * w - 6)
                dot['ypos'].setValue(y + 0.5 *_h - 6)
                dot.setInput(0,node)
                n.setInput(i,dot)
                all_nodes.extend([dot,n])
            elif abs(_x - x)<0.5*(w+_w):
                n['xpos'].setValue(x)
                all_nodes.append(n)
            else:
                n['ypos'].setValue(y)
                all_nodes.append(n)
    return all_nodes


def main():
    node = nuke.selectedNodes()[0]
    all_nodes = tidyUpNodes(node)
    for n in all_nodes:
        n.setSelected(True)


def getInputNodes(node):
    inputs = []
    num_of_inputs = node.inputs
    for i in range(num_of_inputs):
        innode = node.input(i)
        if innode:
            inputs.append((i,innode))
    return inputs


def getOutputNodes(node):
    outputs = []
    parent = node.parent()
    parent.begin()
    all_nodes = nuke.allNodes()
    parent.end()
    for n in all_nodes:
        num_of_inputs = n.inputs()
        for idx  in range(num_of_inputs):
            innode = n.input(idx)
            if innode:
                if innode.name() == node.name():
                    outputs.append((idx,n))
    return outputs