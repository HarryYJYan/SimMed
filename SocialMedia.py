import random
import networkx as nx, numpy as np, pandas as pd
import copy

def constrained_sum_sample_pos(n, m):
    dividers = sorted(random.sample(range(1, m), n - 1))
    return [a - b for a, b in zip(dividers + [m], [0] + dividers)]

def random_graph_revised(n, m):
    degree_squence = constrained_sum_sample_pos(n, m)
    node_ids = list(range(n))
    edge_list = []
    for i in node_ids:
        non_self = [j for j in node_ids if i!= j]
        targets = random.sample(non_self, degree_squence[i]) 
        edges_of_n = [(i,target) for target in targets]
        edge_list = edge_list+ edges_of_n
    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    return G

#G = random_graph_revised(n, m)

### social media 
### social media 
class SocialMedia:
    def __init__(self, n = 100, m = 400):
        self.p = .5
        #self.q = .5
        self.n = n
        self.m = m
        self.l = np.random.randint(2, 10, n)
        self.G = random_graph_revised(self.n,self.m) 
        ### need to make sure there is no node that has zero out degree. 
        
        self.O = np.random.uniform(-1, 1, self.n)
        self.Opinions_db = {"Time_0": copy.deepcopy(self.O)}#pd.DataFrame(self.O, columns= ["Time_0"]) ### uniform distribution
        self.Message_db = pd.DataFrame(columns = ["original_poster", "rt_poster","content", "rt_status"])
        self.Network_db = {"Time_0": list(self.G.edges())}
        self.ME_db = pd.DataFrame(columns = ["uid", "Time", "index", "effects"])
        self.Config_db = {}
        #self.audience = audience
        #self.media_id = ["mainstream_media", "liberal_media", "conservative_media", "extreme_liberal_media", "extreme_conservative_media"]

    def record_sub(self, media_audience):
        return media_audience

    def screen_size(self, uid):
        l = self.l[uid] + np.random.randint(-2, 2) ## hidden parameter
        return l
            
    def make_screen(self, uid, l, sub, include_media = True):
        friends = list(self.G.successors(uid))
        if include_media :
            friends = friends + sub
        #print
        repost_by_friend = self.Message_db.rt_poster.isin(friends)
        #print(repost_by_friend)
        screen = self.Message_db[repost_by_friend].tail(l)
        if len(screen)>0:
            return screen
        else:
            return None
        
    def get_recent_o(self, uid):
        return self.O[uid]

    def get_recent_neighors(self, uid):
        return self.G.successors(uid)
    
    def get_recomm_friends(self, uid, media_ids, eta):
        me_and_friends = set(self.G.successors(uid)).union({uid}).union(media_ids) ### No rewiring of media
        recent = self.Message_db[~self.Message_db.rt_poster.isin(me_and_friends)].tail(self.l[uid]*3) ### hidden parameter
        if len(recent) >0:
            recent["fri_or_foe"] = np.where(np.abs(recent.content.values-self.O[uid]) < eta, True, False)
            recommended = recent[recent.fri_or_foe == True]
            if len(recommended) > 0:
                return recommended


    def add_edge(self, uid, target):
        self.G.add_edge(uid, target)

    def delete_edge(self, uid, target):
        self.G.remove_edge(uid, target)
        
    def add_message(self, messege):
        self.Message_db = pd.concat([self.Message_db,messege], ignore_index = True, axis = 0)
    #########    
    def update_Opinions_db(self, uid, new_o, t):
        if new_o:
            self.O[uid] = new_o
        self.Opinions_db["Time_"+str(t+1)] = copy.deepcopy(self.O)
        #self.Opinions_db = pd.concat([self.Opinions_db, pd.DataFrame(self.O, columns= ["Time_"+str(t)])], axis =1 )

    def update_Network_db(self, t):
        self.Network_db["Time_"+str(t+1)] = copy.deepcopy(list(self.G.edges())) 
    
    def update_ME_db(self,t, uid, fri, foe):
        if fri is not None:
            #print(fri)
            fri = fri.reset_index()
            fri["effects"] = True 
            fri["uid"] = uid
            fri["Time"] = t + 1
            fri_record = fri[["uid", "Time", "index", "effects"]]
            #print(fri_record)
            self.ME_db = pd.concat([self.ME_db, fri_record], axis= 0, ignore_index=True)
            #print(self.ME_db)
        if foe is not None:
            foe = foe.reset_index()
            foe["effects"] = False
            foe["uid"] = uid
            foe["Time"] = t + 1 
            foe_record = foe[["uid", "Time", "index", "effects"]]
            self.ME_db = pd.concat([self.ME_db, foe_record], ignore_index= True)
        #return fri_record, foe_record
        
    def find_media(self, screen):
        if screen is not None:
            bool = (screen.original_poster.str.contains("media") | screen.rt_poster.str.contains("media"))
            found = screen[bool]
            return found
           
