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

            #Ensure nodes does not have 2 edges using the same production rule
            if fr != prev_node:
                current_lang = self.language.copy()
            
            #Randomly selects transition
            trans = np.random.choice(current_lang,replace=True)
            #Removes transition from choices in the case where next edge goes from same node
            current_lang.remove(trans)

            g.add_edge(fr,to,label=str(trans))
            prev_node = fr

        #Uncomment to save image of graph
        #save_dir_png = "test2/" + self.file_name + ".png"
        #A = nx.nx_agraph.to_agraph(g)
        #A.layout(prog='dot')
        #A.draw(save_dir)

        save_dir_txt = "test2/" + self.file_name + ".txt"
        nx.write_edgelist(g,save_dir_txt) 

    
    
if __name__ == "__main__":
    #Maybe replace language with langugae size where it auto generates language upon class init
    for i in range(0,100):    
        g = GraphEdgeGenerator("12/adj/",str(i),["a","b","c","d","e","f"])
        g.calc_trans_paths()
        print(i)
    