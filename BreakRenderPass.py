import nuke,nukescripts
import random

LIGHTPASSES = ('diffuse','globalillumin','lighting','glossy','reflection','coat','transmission','sss','emission','emit','volume')
COLORDICT = {
    'rgba':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(64,190,109,255),16),
    'beauty':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(64,190,109,255),16),
    'diffuse':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(145,145,145,255),16),
    'globalillumin':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(145,145,145,255),16),
    'lighting':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(145,145,145,255),16),
    'glossy' : int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(233,193,37,255),16),
    'reflection':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(233,193,37,255),16),
    'coat':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(171,193,108,255),16),
    'transmission':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(149,97,235,255),16),
    'sss':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(209,152,134,255),16),
    'emission':int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(97,164,217,255),16),
    'emit' : int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(97,164,217,255),16),
    'volume' : int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(141,165,183,255),16),
    'other' : int('{0:0x}{1:0x}{2:0x}{3:0x}'.format(113,40,83,255),16)
}


def prepareForAutoComp(layer_list):
    light_passes = []
    non_light_passes = []
    for light_pass in LIGHTPASSES:
        for n in layer_list:
            if n.lower().find(light_pass)>-1 and (n not in light_passes):
                light_passes.append(n)
                continue


    non_light_passes = [n for n in layer_list if n not in light_passes]
    return light_passes,non_light_passes


def grabLayers(node):
    layers = dict()
    all_channels = node.channels()
    for channel in all_channels:
        layer_name = channel.split('.')[0]
        if layer_name.lower().find('crypto')>=0:
            continue
        channel_name = channel.split('.')[1]
        if layer_name in layers.keys():
            layers[layer_name].append(channel_name)
        else:
            layers[layer_name]=[channel_name]
    light_pass,non_light_passes = prepareForAutoComp(layers.keys())
    return layers,light_pass,non_light_passes


def createMappings(layer,channels):
    mapping = []
    num_of_chan = len(channels)
    if num_of_chan == 1:
        mapping = [(f"{layer}.{channels[0]}",'rgba.red')]
    elif num_of_chan == 2:
        mapping = [(f"{layer}.{channels[0]}","rgba.red"),(f"{layer}.{channels[1]}","rgba.green")]
    elif num_of_chan == 3:
        mapping = [(f"{layer}.{channels[0]}","rgba.red"),(f"{layer}.{channels[1]}","rgba.green"),(f"{layer}.{channels[2]}","rgba.blue")]
    elif num_of_chan == 4:
        mapping = [(f"{layer}.{channels[0]}","rgba.red"),(f"{layer}.{channels[1]}","rgba.green"),(f"{layer}.{channels[2]}","rgba.blue"),(f"{layer}.{channels[3]}","rgba.alpha")]
    return mapping


def createPass(layer,layers):
    shuffle = nuke.nodes.Shuffle2()
    if set(layers[layer]) == set(['red','green','blue']) or set(layers[layer]) == set(['red','green','blue','alpha']):
        shuffle['in1'].setValue(layer)
        shuffle['out1'].setValue('rgba')
        shuffle['in2'].setValue('alpha')
        shuffle['out2'].setValue('alpha')
        shuffle['mappings'].setValue([(1,'rgba.alpha','rgba.alpha')])
    else:
        shuffle['in1'].setValue(layer)
        mapping = createMappings(layer,layers[layer])
        shuffle['mappings'].setValue(mapping)
    shuffle['postage_stamp'].setValue(1)
    label_string = ''
    for i,char in enumerate(layer):
        label_string = label_string + char
        if (i+1)%12==0:
            label_string = label_string + '\n'
    if label_string == 'rgba':
        label_string = 'beauty'
    shuffle['label'].setValue(label_string)
    return shuffle


def breakPasses(node,layers,light_pass,non_light_passes):
    light_node_list = []
    non_light_node_list = []
    if layers:
        for layer in light_pass:
            shuffle = createPass(layer,layers) 
            light_node_list.append(shuffle) 
            shuffle.setInput(0,node)
        for layer in non_light_passes:
            shuffle = createPass(layer,layers) 
            non_light_node_list.append(shuffle) 
            shuffle.setInput(0,node)
    all_nodes = light_node_list + non_light_node_list 
    colorPasses(all_nodes)
    for n in all_nodes:
        x = n.xpos() 
        y = n.ypos() 
        nuke.autoplaceSnap(n) 
        n['xpos'].setValue(x) 
        n['ypos'].setValue(y)
    return light_node_list,non_light_node_list


def colorPasses(node_list):
    keys = COLORDICT.keys()
    for n in node_list:
        layer = n['label'].value().replace('\n', '').lower()
        find = 0
        for key in keys:
            if layer.find(key) > -1:
                n['tile_color'].setValue(COLORDICT[key])
                print(COLORDICT[key])
                find = 1
        if find == 0:
            n['tile_color'].setValue(COLORDICT['other'])


def autoComp(ref_node,light_node_list,non_light_node_list):
    all_nodes = [ref_node]
    h_offset = 120
    v_offset = 20
    x = ref_node.xpos()
    y = ref_node.ypos()
    b_node = light_node_list[0]
    for i,n in enumerate(light_node_list):
        if i == 0:
            n['xpos'].setValue(x)
            n['ypos'].setValue(y+h_offset)
            # nuke.autoplaceSnap(n)
            ref_node = n
            b_node = n
            all_nodes.append(n)
        else:
            x = ref_node.xpos()+h_offset
            y = ref_node.ypos()
            n['xpos'].setValue(x)
            n['ypos'].setValue(y)
            ref_node = n
            # b_node = n
            merge = nuke.nodes.Merge2(operation='plus',Achannels='rgb')
            if (i == 1):
                y = n.ypos()+n.screenHeight()+v_offset+40
            else:
                y = b_node.ypos()+18+v_offset
            merge['xpos'].setValue(x)
            merge['ypos'].setValue(y)
            merge.setInput(0,b_node)
            merge.setInput(1,n)
            b_node = merge
            all_nodes = all_nodes + [n,merge]

    nop = nuke.nodes.NoOp()
    nop.setInput(0,b_node)
    nop.setXpos(b_node.xpos())
    nop.setYpos(b_node.ypos()+18+v_offset)
    all_nodes.append(nop)

    for n in non_light_node_list:
        x = ref_node.xpos()+h_offset
        y = ref_node.ypos()
        n['xpos'].setValue(x)
        n['ypos'].setValue(y)
        ref_node = n
        all_nodes.append(n)

    organizeNodes(all_nodes)
    return all_nodes

def addBackdrop(node_list):
    x0 = node_list[0].xpos()
    y0 = node_list[0].ypos()
    x1 = x0 + node_list[0].screenWidth()
    y1 = y0 + node_list[0].screenHeight()

    for n in node_list:
        x = n.xpos()
        y = n.ypos()
        w = n.screenWidth()
        h = n.screenHeight()

        if x < x0:
            x0 = x
        if y < y0:
            y0 = y
        if x1 < x + w:
            x1 = x + w
        if y1 < y + h:
            y1 = y + h

    backdrop = nuke.nodes.BackdropNode()
    backdrop.setXpos(x0-100)
    backdrop.setYpos(y0-100)
    backdrop['bdwidth'].setValue(x1-x0+200)
    backdrop['bdheight'].setValue(y1-y0+200)
    backdrop["note_font_size"].setValue(75)
    r = random.randint(100,200)
    g = random.randint(100,200)
    b = random.randint(100,200)
    a = 128
    tile_color = int('{0:02x}{1:02x}{2:02x}{3:02x}'.format(r,g,b,a),16)
    backdrop["tile_color"].setValue(tile_color)
    return backdrop


def organizeNodes(node_list):
    for n in node_list:
        max_inputs = n.inputs()
        x = n.xpos()
        y = n.ypos()
        for i in range(max_inputs):
            in_node = n.input(i)
            if in_node:
                in_x = in_node.xpos()
                in_y = in_node.ypos()
                if x != in_x:
                    dot = nuke.nodes.Dot()
                    # nuke.autoplaceSnap(dot)
                    name = n.name()
                    if name.startswith("Shuffle"):
                        dot['xpos'].setValue(x + 80 * 0.5 - dot.screenWidth()/2.0) 
                        dot['ypos'].setValue(in_y + in_node.screenHeight()/2.0 - dot.screenHeight()/2.0)
                    else:
                        dot['xpos'].setValue(in_x + in_node.screenWidth()/2.0 - dot.screenWidth()/2.0 )
                        dot['ypos'].setValue(y + n.screenHeight()/2.0 - dot.screenHeight()/2.0)
                    dot.setInput(0, in_node)
                    n.setInput(0, dot)

def main():
    node = nuke.selectedNodes()[0]
    layers, light_pass, non_light_passes = grabLayers(node)
    light_node_list, non_light_node_list = breakPasses(node,layers,light_pass,non_light_passes)
    # print(light_node_list,non_light_node_list)
    if len(light_node_list) > 0:
        all_nodes = autoComp(node, light_node_list, non_light_node_list)
    else:
        all_nodes = non_light_node_list
    backdrop = addBackdrop([node] + all_nodes)
    nuke.show(backdrop)


# main()

