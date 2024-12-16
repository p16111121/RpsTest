# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random
import itertools
beat = {'R': 'P', 'P': 'S', 'S': 'R'} #規則

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    global history,output,models
#定義馬可夫鏈模型
    class MarkovChain():

        def __init__(self, type, beat, level, memory, score=0, score_mem=0.9):
            self.type = type #模型類型
            self.matrix = self.create_matrix(beat, level, memory) 
            self.memory = memory #記憶權重，對於記憶的重視程度
            self.level = level #歷史模式的層級
            self.beat = beat
            self.score = score #分數 評估模型表現
            self.score_mem = score_mem #分數記憶權重，控制模型分數更新時的衰減
            self.prediction = ''
            self.name = 'level: {}, memory: {}'.format(self.level, self.memory)
            self.last_updated_key = ''  
    #創建機率矩陣 生成所有可能的歷史組合（如 "R", "P", "S", "RP", "RS" 等）
        @staticmethod
        def create_matrix(beat, level, memory):

            def create_keys(beat, level):
                keys = list(beat)

                if level > 1:

                    for i in range(level - 1):
                        key_len = len(keys)
                        for i in itertools.product(keys, ''.join(beat)):
                            keys.append(''.join(i))
                        keys = keys[key_len:]

                return keys

            keys = create_keys(beat, level)

            matrix = {} # 分配初始概率，所有出招（R、P、S）的初始概率均相等
            for key in keys:
                matrix[key] = {'R': 1 / (1 - memory) / 3,
                               'P': 1 / (1 - memory) / 3,
                               'S': 1 / (1 - memory) / 3}

            return matrix   
    # 更新機率矩陣，調整出招機率
        def update_matrix(self, key_lagged, response):

            for key in self.matrix[key_lagged]:
                self.matrix[key_lagged][key] = self.memory * self.matrix[key_lagged][key]

            self.matrix[key_lagged][response] += 1
            self.last_updated_key = key_lagged  
    # 更新分數
        def update_score(self, inp, out):

            if self.beat[out] == inp:
                self.score = self.score * self.score_mem - 1
            elif out == inp:
                self.score = self.score * self.score_mem
            else:
                self.score = self.score * self.score_mem + 1    
    # 預測對手行為
        def predict(self, key_current):

            probs = self.matrix[key_current]

            if max(probs.values()) == min(probs.values()):
                self.prediction = random.choice(list(beat.keys()))
            else:
                self.prediction = max([(i[1], i[0]) for i in probs.items()])[1]

            if self.type == 'input_oriented':
                return self.prediction
            elif self.type == 'output_oriented':
                return self.beat[self.prediction    ]

    #定義集成模型，結合多個馬爾可夫模型的輸出，通過加權平均來得出最終預測
    class Ensembler():
        def __init__(self, type, beat, min_score=-10, score=0, score_mem=0.9):
            self.type = type
            self.matrix = {i: 0 for i in beat}
            self.beat = beat
            self.min_score = min_score
            self.score = score
            self.score_mem = score_mem
            self.prediction = ''

        def update_score(self, inp, out):

            if self.beat[out] == inp:
                self.score = self.score * self.score_mem - 1
            elif out == inp:
                self.score = self.score * self.score_mem
            else:
                self.score = self.score * self.score_mem + 1

        def update_matrix(self, pred_dict, pred_score):
            norm_dict = {key: pred_dict[key] / sum(pred_dict.values()) for key in pred_dict}
            for key in self.matrix:
                if pred_score >= self.min_score:
                    self.matrix[key] = self.matrix[key] + pred_score * norm_dict[key]

        def predict(self):

            if max(self.matrix.values()) == min(self.matrix.values()):
                self.prediction = random.choice(list(beat.keys()))
            else:
                self.prediction = max([(i[1], i[0]) for i in self.matrix.items()])[1]

            return self.prediction

    # 歷史收集器，僅保留最近10回合的紀錄
    class HistoryColl():
        def __init__(self):
            self.history = ''

        def hist_collector(self, inp, out):
            self.history = self.history + inp
            self.history = self.history + out
            if len(self.history) > 10:
                self.history = self.history[-10:]

        def create_keys(self, level):
            return self.history[-level:]

        def create_keys_hist(self, level):
            key_hist = self.history[-level - 2:-2]
            inp_latest = self.history[-2]
            out_latest = self.history[-1]
            return key_hist, inp_latest, out_latest

    #第一回合 隨機出招 並創建模型
    if len(opponent_history) <= 1:

        output = random.choice(list(beat.keys()))   
        history = HistoryColl() 
        memory = [0.5, 0.6, 0.7, 0.8, 0.9, 0.93, 0.95, 0.97, 0.99]
        level = [1, 2, 3, 4]
        ensemble_min_score = [5]    
        models_inp = [MarkovChain('input_oriented', beat, i[0], i[1]) for i in itertools.product(level, memory)]
        models_out = [MarkovChain('output_oriented', beat, i[0], i[1]) for i in itertools.product(level, memory)]
        models_ens = [Ensembler('ensemble', beat, i) for i in ensemble_min_score]   
        models = models_inp + models_out + models_ens

    elif len(opponent_history) >= 10:

       history.hist_collector(prev_play, output)

       max_score = 0

       for model in models:

           if model.type in ('input_oriented', 'output_oriented'):
               key_hist, inp_latest, out_latest = history.create_keys_hist(model.level)
               key_curr = history.create_keys(model.level)

           if model.prediction != '':
               model.update_score(prev_play, beat[model.prediction])

           if model.type == 'input_oriented':
               model.update_matrix(key_hist, inp_latest)

           elif model.type == 'output_oriented':
               model.update_matrix(key_hist, out_latest)

           elif model.type == 'ensemble':
               for mod in models:
                   if mod.type in ('input_oriented', 'output_oriented'):
                       model.update_matrix(mod.matrix[mod.last_updated_key], model.score)

           if model.type in ('input_oriented', 'output_oriented'):
               predicted_input = model.predict(key_curr)
           elif model.type == 'ensemble':
               predicted_input = model.predict()

           if model.score > max_score:
               best_model = model
               max_score = model.score
               output = beat[predicted_input]

       if max_score < 1:
           output = random.choice(list(beat.keys()))

    else:
        history.hist_collector(prev_play, output)
        output = random.choice(list(beat.keys()))

    return output
