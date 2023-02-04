import networkx as nx
import random
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz as pgv

#Completely random selection of edges
#Constraints ensure graph is Directed and acyclic

class GraphGenerator:
    def __init__(self,num_edges,num_paths,min_path_length,max_itr):
        self.num_edges = num_edges
        self.num_paths = num_paths
        self.min_path_length = min_path_length
        self.max_itr = max_itr

    def init_graph(self,g):
        g.add_node(0,style='filled',fillcolor='red')
        g.add_node(self.num_edges,style='filled',fillcolor='red')
        for i in range(1,self.num_edges-1):
            g.add_node(i)
        return g

    def gen_graph(self):
        print(self.num_edges)
        g = nx.DiGraph()
        g = self.init_graph(g)
        i = 0
        while((self.total_paths(g) < self.num_paths) and (i < self.max_itr)):
            i = i + 1
            fr = random.randint(0,self.num_edges-1)
            to = random.randint(1,self.num_edges)

            if(nx.is_path(g,[fr,to]) == True):
                continue
            #if(nx.has_path(g,0,fr) == False):
            #    continue

            new_g = g.copy()
            new_g.add_edge(fr,to)
            if (self.is_cycle(new_g) == False) and (self.min_path_length <= self.current_min_path_length(g)):
                g = new_g
            else:
                print('cycle')
                continue
            print(i)
        print('Complete')
        A = nx.nx_agraph.to_agraph(g)
        A.layout(prog='dot')
        A.draw('test.png')
        
    def total_paths(self,g):
        try:
            path = list(nx.all_shortest_paths(g,0,self.num_edges))
            filtered_paths = [x for x in path if len(x) >= self.min_path_length]
            print('PATH',path)
            print('FILTERED PATH', filtered_paths)
            return len(path) 
        except:
            return 0     

    def current_min_path_length(self,g):
        try:
            paths = list(nx.all_shortest_paths(g,0,self.num_edges))
            path_lengths = map(len(),paths)
            return min(path_lengths)
        except:
            return self.min_path_length + 1 #If there are no current paths

    def is_cycle(self,g):
        return not nx.is_directed_acyclic_graph(g)

if __name__ == "__main__":
    f = GraphGenerator(20,1,5,300)
    f.gen_graph()