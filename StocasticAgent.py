import networkx as nx
import random

#Equation used to calc P('user selects action' | 'possible actions')
#Uniform distribution means action is randomly selected
#P(X=x|Y) = 1 / |Y| where Y is a subset of L (language)

class StocasticAgent:
    def __init__(self,language):
        self.language = language
    
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
        return random.choice(self.trans_paths)
     
    def get_possible_prov_paths(self):
        return self.trans_paths        

        
    #Saves graph as image for testing
    def save_graph_pic(self):
        A = nx.nx_agraph.to_agraph(self.g)
        A.layout(prog='dot')
        A.draw("test/test.png")

if __name__ == "__main__":
    agent = StocasticAgent(["a","b","c","d","e","f"])
    agent.load_graph("test2/5.txt")
    #agent.save_graph_pic()
    print(agent.calc_pp_paths())
    print(agent.trans_paths)
    print(agent.calc_prov_path())

