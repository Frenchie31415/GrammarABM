import networkx as nx
import random
import numpy as np

#Equation used to calc P('user selects action' | 'possible actions')
#P(E=e|P) = product(P(X=x)) for x in E (Assumes transformations are independent of each other)

class LinearActAgent:
    def __init__(self,language):
        self.language = language
    
    def gen_dist(self):
        num_trans = len(self.language)
        dist = []
        
        for i in range(0,num_trans):
            dist.append(random.randint(0,100)) #If =0 then agent is unaware of transformation

        self.dist = dist
    
    def load_graph(self,dir):
        self.g = nx.read_edgelist(dir,create_using=nx.DiGraph)

    def calc_pp_paths(self):
        end_node = self.g.number_of_nodes() - 1
        paths = list(nx.all_simple_paths(self.g,str(0),str(end_node)))
        trans_paths = []
        for path in paths:
            trans_path = ""
            for i in range(0,len(path)-1):
                fr = path[i]
                to = path[i+1]
                dict = self.g.get_edge_data(fr,to)
                trans_path = trans_path + dict['label']
            trans_paths.append(trans_path)
        self.trans_paths = trans_paths

    def calc_prov_path(self):
        paths = self.trans_paths.copy()
        
        paths_prob = list(map(self.calc_prob,paths)) #Calcs Prob of each path
        cumulative = sum(paths_prob)

        for i in range(0,len(paths_prob)):
            paths_prob[i] = paths_prob[i] / cumulative

        actual_path = np.random.choice(paths,p=paths_prob)

        return actual_path
     
    def get_possible_prov_paths(self):
        return self.trans_paths        
    
    #Calc Prob of a possible path
    def calc_prob(self,path):
        path_prob = 0
        weight = 0.1
        coef = 1 + (len(path) - 1) * weight
        for trans in path:
            trans_index = self.language.index(trans)
            path_prob = path_prob + (self.dist[trans_index] * coef)
            coef = coef - 0.1
        return path_prob

        
    #Saves graph as image for testing
    def save_graph_pic(self):
        A = nx.nx_agraph.to_agraph(self.g)
        A.layout(prog='dot')
        A.draw("test/test.png")

if __name__ == "__main__":
    agent = LinearActAgent(["a","b","c","d","e","f"])
    agent.gen_dist()
    agent.load_graph("test2/0.txt")
    #agent.save_graph_pic()
    agent.calc_pp_paths()
    agent.calc_prov_path()

