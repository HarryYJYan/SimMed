import numpy as np, pandas as pd
import copy

class MassMedia():
    def __init__(self, p,  s, n, agents = 100):
        self.p = p
        self.s = s
        self.n = n
        self.agents = agents
        self.mids = ["m"+str(i) for i in range(n)]
        self.shares = self.init_share()
        self.init_subs = self.split_list()#self.random_split() #
        self.subs = {self.mids[i]:self.init_subs[i] for i in range(n)} #self.split_list()
        self.Subs_db = {"Time_0": copy.deepcopy(self.subs)}
        #self.messege_db = {"Time_0": {self.mids[i]:[] for i in range(n)}}
        
    def init_share(self):
        holders = np.ones (self.agents)
        splits = np.random.choice(np.arange(1,self.agents), self.n-1, replace=False)
        splits = [0] + list(sorted(splits)) + [self.agents]
        return [int(np.sum(holders[splits[i]:splits[i+1]])) for i in range(self.n)] 
    
    def split_list(self): ### No overlap
        start = 0
        end = 0
        output = []
        aud_size =  int(np.ceil(self.agents * self.s))
        aud_ids = np.random.choice(np.arange(self.agents), aud_size, replace= False)
        sizes = np.int32(np.ceil(np.array(self.shares)*self.s))
        for size in sizes:
            end += size
            output.append(aud_ids[start:end])
            start = end
        return output
    
    def random_split(self): ## With possible overlap
        aud_size =  int(np.ceil(self.agents * self.s))
        aud_ids = np.random.choice(np.arange(self.agents), aud_size, replace= False)
        sizes = np.int32(np.ceil(np.array(self.shares)*self.s))
        return [np.random.choice(aud_ids, size, replace= False) for size in sizes ]
    
    def media_messege(self, mid, Os, d = .25):
        if np.random.rand() < self.p:
            recent = self.Subs_db[list(self.Subs_db.keys())[-1]]
            v = np.mean(Os[recent[mid]]) + d*(np.random.rand() -1)
            post = pd.DataFrame({"original_poster": [mid], "rt_poster": [mid], "content": [v], "rt_status":[False]})
            return post
        else:
            return None
    
    def find_subs(self, uid):
        subs = [k for k, v in self.subs.items() if uid in v]
        return subs
        
    def cancel(self, uid, foe_target):
        self.subs[foe_target] = self.subs[foe_target][self.subs[foe_target] !=uid]
    
    def subscribe(self, uid, fri_target):
        if uid not in self.subs[fri_target]:
            self.subs[fri_target] = np.append(self.subs[fri_target], uid)

    def update_Sub_DB(self, t):
        self.Subs_db["Time_{}".format(t)] =  copy.deepcopy(self.subs)


        

