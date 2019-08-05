import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from FBA import settings 
import os
import hashlib
import pandas as pd

def draw_cycle(reaction):
    md5 = hashlib.md5()
    md5.update(bytes(str(reaction),encoding="utf-8"))
    hash_str = md5.hexdigest()

    var = re.split('\s|/',reaction)   
    reaction = var[:-1]
    plt.switch_backend("agg")
    fig = plt.figure()
    if len(reaction) > 18:
        length = (len(reaction) -18) *0.2 + 6.4
        width = (len(reaction)-18)* 0.15 + 6.4
        fig.set_size_inches(length,width,forward=True)
    num = var[-1]
    reaction_list = [tuple(reaction[i:i+2]) for i in range(0,len(reaction)-1)]
    reaction_list.append((reaction[-1],reaction[0]))
    G = nx.DiGraph() # 空图
    G.add_edges_from(reaction_list)
    G.add_node(num)

    theta = np.linspace(0,2*np.pi,len(reaction)+1)
    theta = theta[:-1]
    r = [25] * len(reaction)
    X = list(map(lambda x,y:x*np.cos(y),r,theta))
    Y = list(map(lambda x,y:x*np.sin(y),r,theta))
    cart = list(map(lambda x,y:[x,y],X,Y))
    cart.append([0,0])
    fixed_position = dict(zip(var,cart))
    num = var[-1]
    R,M,O = {},{},{}
    for node in G.nodes:
        R_result = re.match("R_",node)
        M_result = re.match("M_",node)
        if R_result:
            R[node]=node
        elif M_result:
            M[node]=node
        else:
            O[node]=node

    nx.draw_networkx(G,fixed_position,node_color="white",edge_color="grey",with_labels=False)
    nx.draw_networkx_labels(G,fixed_position,R,font_size=8,font_color="blue")
    nx.draw_networkx_labels(G,fixed_position,M,font_size=8,font_color="red")
    nx.draw_networkx_labels(G,fixed_position,O,font_size=10,font_color="black")
    plt.axis("off")
    image_name = "%s.png"%hash_str
    path =  "%s/%s/%s"%(settings.MEDIA_ROOT,"image",image_name)
    fig.savefig(path,dpi=300)

    return image_name

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path= os.path.join(path,i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def to_file(param):
    product = param[param["role"]=="product"]
    product["process"] = product["reaction"] + " -> " + product["stoich"] + " " + product["species"] + ";" + product["values"]
    substrate = param[param["role"]=="substrate"]
    print(product)
    substrate["process"] = substrate["stoich"] + " " + substrate["species"] + " -> " + substrate["reaction"] + ";" + substrate["values"]
    pro_sub = pd.concat([product,substrate])
    pro_sub = pro_sub[["process"]]
    return pro_sub

