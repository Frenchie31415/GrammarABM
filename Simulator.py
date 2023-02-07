import random
from Agent import Agent
from Model import Model

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
        self.possible_provenance = []
        future = []
        for i in self.test:
            path = self.dir + str(i) + ".txt"
            self.agent.load_graph(path)
            self.agent.calc_pp_paths()
            self.possible_provenance.append(self.agent.get_possible_prov_paths())
            future.append(self.agent.calc_prov_path())
        self.future = future
    
    def predict_prov_future(self):
        model = Model(["a","b","c","d","e","f"],self.history)
        model.calc_freq_dist()
        predicted_future = []
        for i in self.possible_provenance:
            predicted_future.append(model.predict_prov_path(i))
        self.predicted_future = predicted_future
    
    def print_history_dist(self):
        print("Total trans", len(self.history))
        print("a",self.history.count("a"))
        print("b",self.history.count("b"))
        print("c",self.history.count("c"))
        print("d",self.history.count("d"))
        print("e",self.history.count("e"))
        print("f",self.history.count("f"))

    def eval(self):
        correct = 0
        incorrect = 0
        for i in range(0,len(self.future)):
            actual = self.future[i]
            predicted = self.predicted_future[i]

            if actual == predicted:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        
        return(correct / (correct + incorrect))

if __name__ == "__main__":
    results = []

    for i in range(0,5):
        sim = Simulator("test2/")
        sim.gen_agent_prov_history()
        sim.gen_agent_prov_future()
        sim.predict_prov_future()
        results.append(sim.eval())
    
    print('ACCURACY RESULT')
    print(sum(results) / 5)

