import random
from Agent import Agent
from StocasticAgent import StocasticAgent
from UnaryProbAgent import UnaryProbAgent
from IndActAgent import IndActAgent
from LinearActAgent import LinearActAgent
from PowerActAgent import PowerActAgent
from Model import Model
from Model2 import Model2
from Model3 import Model3
import itertools
import enchant

class Simulator:
    def __init__(self,dir):
        self.dir = dir

        #Initialise agent
        self.agent = UnaryProbAgent(["a","b","c","d","e","f"])
        #self.agent.gen_precedence()
        self.agent.gen_dist()
        self.init_data()

    #Create 5 folds for cross validation
    def init_data(self):
        all_graphs = list(range(0,100))
        #Train test split for graphs
        random.shuffle(all_graphs)
        self.splits = [all_graphs[0:19],all_graphs[20:39],all_graphs[40:59],all_graphs[60:79],all_graphs[80:99]]
        self.test_split = 0
        self.train = all_graphs[20:]
        self.test = all_graphs[:80]

    #Rotates testing fold for cross validation
    def next_fold(self):
        splits = self.splits.copy()
        #Needs to be mod
        self.test_split = self.test_split + 1
        
        self.test = splits[self.test_split % 5]
        del splits[(self.test_split % 5)]
        self.train = list(itertools.chain.from_iterable(splits))

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
        model = Model3(["a","b","c","d","e","f"],self.history)
        model.calc_freq_dist_history() #Used for Model2/3
        model.calc_bin_freq_dist_history() #Used for Model2
        #model.calc_freq_dist() #Used for Model
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
        if len(self.predicted_future) != len(self.future): raise Exception("Different number of paths being compared")
        return self.eval_levenshtein()
    
    def eval_case_by_case(self):
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

    def eval_levenshtein(self):
        #concat history and future
        print("Evaluating")
        future_concat = str(list(itertools.chain.from_iterable(self.future)))
        predicted_future_concat = str(list(itertools.chain.from_iterable(self.predicted_future)))
        longest = max(len(future_concat),len(predicted_future_concat))
        edit_distance = enchant.utils.levenshtein(predicted_future_concat, future_concat)
        return (longest - edit_distance) / longest

    def get_dist_func(self,path):
        dist = []
        dist.append(path.count("a"))
        dist.append(path.count("b"))
        dist.append(path.count("c"))
        dist.append(path.count("d"))
        dist.append(path.count("e"))
        dist.append(path.count("f"))
        return dist
    
    def eval_dist_diff_distance(self):
        future_concat = str(list(itertools.chain.from_iterable(self.future)))
        predicted_future_concat = str(list(itertools.chain.from_iterable(self.predicted_future)))
        future_dist = self.get_dist_func(future_concat)
        predicted_dist = self.get_dist_func(predicted_future_concat)

        cum = 0
        for i in range(0,len(future_dist)):
            cum = cum + (future_dist[i] - predicted_dist[i]) ** 2
        
        return cum ** 0.5

if __name__ == "__main__":
    results = []
    results_lev = []
    results_dist_diff = []
    sim = Simulator("test2/")

    for i in range(0,5):
        sim.gen_agent_prov_history()
        sim.gen_agent_prov_future()
        sim.predict_prov_future()
        results.append(sim.eval_case_by_case())
        results_lev.append(sim.eval_levenshtein())
        results_dist_diff.append(sim.eval_dist_diff_distance())
        sim.next_fold()
    
    print('ACCURACY RESULT')
    print(sum(results) / 5)
    print('LEV RESULTS')
    print(sum(results_lev) / 5)
    print('DIST DIFF RESULTS')
    print(sum(results_dist_diff) / 5)