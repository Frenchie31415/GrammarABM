import networkx as nx
import random
from random import randrange
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz as pgv

#Completely random selection of edges
#Constraints ensure graph is Directed and acyclic

class GraphGenerator:
    def __init__(self,num_nodes,num_paths,min_path_length,min_avg_node_deg,max_itr,file_name):
        self.num_nodes = num_nodes
        self.num_paths = num_paths
        self.min_path_length = min_path_length
        self.min_avg_node_deg= min_avg_node_deg
        self.max_itr = max_itr
        self.file_name = file_name

    def init_graph(self,g):
        g.add_node(0,style='filled',fillcolor='red')
        g.add_node(self.num_nodes,style='filled',fillcolor='red')
        for i in range(1,self.num_nodes):
            g.add_node(i)
        return g

    def gen_graph(self):
        g = nx.DiGraph()
        g = self.init_graph(g)
        i = 0
        pointing = [0]
        while((self.total_paths(g) < self.num_paths) and (i < self.max_itr)):

            if(self.total_paths(g) == self.num_paths):
                break

            i = i + 1
            fr_index = randrange(len(pointing))
            fr = pointing[fr_index]
            to = random.randint(1,self.num_nodes)
            if(nx.is_path(g,[fr,to]) == True): #Ensure edge does not exist
                continue
            if(fr == 0 and to == self.num_nodes): #Ensures start node does not point to end
                continue
            if(fr == self.num_nodes): #Ensures final node is not pointing
                continue
            if((to == self.num_nodes) & (nx.shortest_path_length(g,0,fr) < self.min_path_length - 1)): #Ensure min path length holds
                continue
            #if((to == self.num_nodes) & (self.min_avg_node_deg >= self.graph_avg_node_density(pointing,g))): #Ensure graph has minium average density
            #    continue


            new_g = g.copy()
            new_g.add_edge(fr,to)
            if (self.is_cycle(new_g) == False) and (self.min_path_length <= self.current_min_path_length(new_g)):
                g = new_g
                pointing = pointing + [to]
            else:
                continue

        path = []
        try:
            path = list(nx.all_shortest_paths(g,0,self.num_nodes))
            nodes_used = sorted(list(set().union(*path)))
            new_labels = range(0,len(nodes_used))
            #MAKE DICT FOR RENAMING NODES TO CORRECT NAMES
            mapping = {nodes_used[i]: new_labels[i] for i in range(len(nodes_used))}

            for i in range(self.num_nodes):
                if i not in nodes_used:
                    g.remove_node(i)
            
            print(path)
            g = nx.relabel_nodes(g,mapping)
            nx.write_edgelist(g, "test.txt")
            A = nx.nx_agraph.to_agraph(g)
            A.layout(prog='dot')
            A.draw(self.file_name)
        except:
            print('Generation failed. Trying again...')
            self.gen_graph()
        
    def total_paths(self,g):
        try:
            path = list(nx.all_shortest_paths(g,0,self.num_nodes))
            filtered_paths = [x for x in path if len(x) >= self.min_path_length]
            return len(filtered_paths) 
        except:
            return 0     

    def current_min_path_length(self,g):
        try:
            paths = list(nx.all_shortest_paths(g,0,self.num_nodes))
            path_lengths = map(len(),paths)
            return min(path_lengths)
        except:
            return self.min_path_length + 1 #If there are no current paths

    def is_cycle(self,g):
        return not nx.is_directed_acyclic_graph(g)

    def graph_avg_node_density(self,pointing,g):
        try:
            e = g.number_of_edges()
            v = len(pointing)
            return e / v
        except:
            return 0



if __name__ == "__main__":
    #num_nodes generated (not used)
    #num_paths = number of paths in from 0 -> N
    #min_path_length = min number of nodes in each path
    #min_avg_node_density = miniumum average node density (CURRENTLY COMMENTED OUT)
    #num_itr = max number of edges to be drawn (if num paths is not satisfied)
    #filename - to save dag graph
    for i in range(20):
        filename = "test/test" + str(i) + ".png"
        f = GraphGenerator(30,2,7,0.8,2000,filename)
        f.gen_graph()