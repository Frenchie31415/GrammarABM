import networkx as nx
import random
import numpy as np

#Equation used to calc P('user selects action' | 'possible actions')
#P(X=x|Y) = dist[x] / sum(Y) where Y is a subset of L (language)

class UnaryProbAgent:
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
        num_paths = len(self.trans_paths)
        longest_list = min([len(x) for x in self.trans_paths])
        
        #Iterate over longest path
        for i in range(0,longest_list):
            if num_paths == 1:
                break

            poss_trans = []
            #Get all prov path transitions for that index
            for j in range(0,num_paths):
                poss_trans.append(paths[j][i])
            
            #If all transformations are the same
            if len(set(poss_trans)) == 1:
                continue
            
            #Get transformation with highest precedence
            prec = self.get_prec(poss_trans)
            to_remove = []

            #Get list of paths that don't have highest precedence transformation
            for k in range(0,len(poss_trans)):
                if poss_trans[k] != prec:
                    to_remove.append(k)

            #Remove paths that don't have highest precedence transformation
            for l in sorted(to_remove,reverse=True):
                del paths[l]

            #Update number of paths
            num_paths = num_paths - len(to_remove)
        
        return paths[0]
     
    def get_possible_prov_paths(self):
        return self.trans_paths        
    
    #Determines agents most likely transition out of multiple options in list
    def get_prec(self,list):
        indexes = []
        dist = []
        for i in list:
            index = self.language.index(i)
            indexes.append(index)
            dist.append(index)
        
        total = sum(dist)
        #Creates prob dist for list
        for i in range(0,len(dist)):
            dist[i] = dist[i] / total
        
        return np.random.choice(list,p=dist)

        
    #Saves graph as image for testing
    def save_graph_pic(self):
        A = nx.nx_agraph.to_agraph(self.g)
        A.layout(prog='dot')
        A.draw("test/test.png")

if __name__ == "__main__":
    agent = UnaryProbAgent(["a","b","c","d","e","f"])
    agent.gen_dist()
    agent.load_graph("test2/0.txt")
    #agent.save_graph_pic()
    print(agent.language)
    print(agent.dist)
    agent.calc_pp_paths()
    print(agent.trans_paths)
    print(agent.calc_prov_path())

