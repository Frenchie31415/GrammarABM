import networkx as nx
import random

class Agent:
    def __init__(self,language):
        self.language = language
    
    def gen_precedence(self):
        self.prec = self.language.copy()
        random.shuffle(self.prec)
    
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
        prec_trans = list[0]
        prec_index = self.prec.index(prec_trans)
        for i in range(1,len(list)):
            trans = list[i]
            i_index = self.prec.index(trans)
            if i_index < prec_index:
                prec_trans = trans
                prec_index = i_index
        return prec_trans

        
    #Saves graph as image for testing
    def save_graph_pic(self):
        A = nx.nx_agraph.to_agraph(self.g)
        A.layout(prog='dot')
        A.draw("test/test.png")

if __name__ == "__main__":
    agent = Agent(["a","b","c","d","e","f"])
    agent.gen_precedence()
    agent.load_graph("test2/0.txt")
    #agent.save_graph_pic()
    agent.calc_pp_paths()
    agent.calc_prov_path()

