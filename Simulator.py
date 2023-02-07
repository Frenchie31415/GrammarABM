import random
from Agent import Agent

class Simulator:
    def __init__(self,dir):
        self.dir = dir
        all_graphs = list(range(0,100))

        #Train test split for graphs
        random.shuffle(all_graphs)
        self.train = all_graphs[20:]
        self.test = all_graphs[:80]

        #Initialise agent
        self.agent = Agent(["a","b","c","d","e","f"])
        self.agent.gen_precedence()

    def gen_agent_prov_history(self):
        history = ""
        for i in self.train:
            path = self.dir + str(i) + ".txt"
            self.agent.load_graph(path)
            self.agent.calc_pp_paths()
            history = history + self.agent.calc_prov_path()
        self.history = history

    def gen_agent_prov_future(self):
        future = ""
        for i in self.test:
            path = self.dir + str(i) + ".txt"
            self.agent.load_graph(path)
            self.agent.calc_pp_paths()
            future = future + self.agent.calc_prov_path()
        self.future = future
        print(self.future)
        
    
    def print_history_dist(self):
        print("Total trans", len(self.history))
        print("a",self.history.count("a"))
        print("b",self.history.count("b"))
        print("c",self.history.count("c"))
        print("d",self.history.count("d"))
        print("e",self.history.count("e"))
        print("f",self.history.count("f"))

if __name__ == "__main__":
    sim = Simulator("test2/")
    sim.gen_agent_prov_history()
    sim.gen_agent_prov_future()

