#Based off frequency distribution of characters
class Model:
    def __init__(self,language,history):
        self.language = language
        self.history = history

    def predict_prov_path(self,trans_paths):
        paths = trans_paths.copy()
        num_paths = len(trans_paths)
        longest_list = min([len(x) for x in trans_paths])
        
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

    def calc_freq_dist(self):
        self.freqs = []
        for i in self.language:
            freq = self.history.count(i) #Frequency of transition
            self.freqs.append(freq)
    
    def get_prec(self,list):
        prec_trans = list[0]
        prec_index = self.language.index(prec_trans)
        for i in range(1,len(list)):
            trans = list[i]
            i_index = self.language.index(trans)
            if self.freqs[i_index] > self.freqs[prec_index]:
                prec_trans = trans
                prec_index = i_index
        return prec_trans
