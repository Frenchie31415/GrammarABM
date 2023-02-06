import random 
import numpy as np
import networkx as nx
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz as pgv

class GraphEdgeGenerator:

    def __init__(self, dir,file_name,language):
        self.dir = dir
        self.file_name = file_name
        self.language = language
    
    #Returns g the read graph
    def calc_trans_paths(self):
        g = nx.DiGraph()
        path = self.dir + "/" + self.file_name + ".txt"
        f = open(path,'r')
        lines = f.readlines()

        prev_node = 0
        current_lang = self.language.copy()
        
        for line in lines:
            nodes = line.split(" ")
            fr = int(nodes[0])
            to = int(nodes[1])

            if fr != prev_node:
                current_lang = self.language.copy()
            
            trans = np.random.choice(current_lang,replace=True)
            current_lang.remove(trans)

            if(g.has_node(fr) == False):
                g.add_node(fr)
            if(g.has_node(to) == False):
                g.add_node(to)

            g.add_edge(fr,to,label=str(trans))
            prev_node = fr

        A = nx.nx_agraph.to_agraph(g)
        A.layout(prog='dot')
        A.draw("test/" + "0.png")
        end_node = g.number_of_nodes() - 1
        paths = list(nx.all_simple_paths(g,0,end_node))
        trans_paths = []
        for path in paths:
            trans_path = ""
            for i in range(0,len(path)-1):
                fr = path[i]
                to = path[i+1]
                dict = g.get_edge_data(fr,to)
                trans_path = trans_path + dict['label']
            trans_paths.append(trans_path)

    
    
if __name__ == "__main__":
    g = GraphEdgeGenerator("12/adj/","6",["a","b","c","d","e","f"])
    g.calc_trans_paths()
    