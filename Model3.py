import numpy as np
#Selects path with the minimum angle between vector reps of frequency
class Model3:
    def __init__(self,language,history):
        self.language = language
        self.history = history

    def predict_prov_path(self,trans_paths):
        paths = trans_paths.copy()
        
        paths_freqs = list(map(self.calc_bin_freq_dist,paths))
        paths_angle = list(map(self.calc_angle,paths_freqs))
        predicted_path_index = min(range(len(paths_angle)), key=paths_angle.__getitem__)

        return paths[predicted_path_index]

    def calc_angle(self,path_dist):
        v1 = self.unit_vector(self.bin_freqs)
        v2 = self.unit_vector(path_dist)

        return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)

    def calc_freq_dist_history(self):
        self.freqs = []
        for i in self.language:
            freq = self.history.count(i) #Frequency of transition
            self.freqs.append(freq)

    def calc_bin_freq_dist_history(self):
        self.bin_freqs = []

        for i in self.language:
            for j in self.language:
                sub_str = i + j
                self.bin_freqs.append(self.history.count(sub_str))

    def calc_bin_freq_dist(self,list):
        freqs = []
        for i in self.language:
            for j in self.language:
                sub_str = i + j
                freqs.append(list.count(sub_str))

        return freqs
    
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
