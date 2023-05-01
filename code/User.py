import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np, pandas as pd

class User():
    def __init__ (self, uid, eta, miu, o, G, subs, mids):
        self.uid = uid
        self.eta = eta
        self.miu = miu
        self.o = o
        self.G = G
        self.f = self.G.successors(uid)
        self.subs = subs
        self.mids = mids
        self.me_fri_subs = set(self.f).union({self.uid}).union(self.subs)


    def find_fri(self, screen):
        if screen is not None:
            screen["fri_or_foe"] = np.where(np.abs(screen.content.values-self.o)<self.eta, True, False)
            fri = screen[screen.fri_or_foe == True]
            if len (fri) >0:
                return fri
            else:
                return None
    
    def find_foe(self, screen):
        if screen is not None:
            screen["fri_or_foe"] = np.where(np.abs(screen.content.values-self.o)<self.eta, True, False)
            foe = screen[screen.fri_or_foe == False]
            if len (foe) >0:
                return foe
            else:
                return None
 
    def update_opinion(self,fri, rand):
        if fri is not None:
            social_influence = self.miu * np.mean(fri.content - self.o)
            new_opinion = self.o+ social_influence + (np.random.random()*2-1)*rand
            ##self.o = new_opinion >>> this is somewhat critical: including this that means all of posts, friending, and unfriending will based on the new opinion
            return new_opinion

    def generate_post(self, fri, p = .5):
        if np.random.random()< p:
            if fri is not None:
                rt = fri.sample(1)
                rt["rt_poster"] = self.uid
                rt["rt_status"] = True
                rt.drop(["fri_or_foe"], axis = 1, inplace = True)
                #print("Agent {} repost {}".format(str(self.uid), str(rt.original_poster)))
                return rt    
        else:
            self_tw = pd.DataFrame({"original_poster": [self.uid], "rt_poster": [self.uid], "content": [self.o], "rt_status":[False]})
            #print("Agent {} post about self".format(str(self.uid)))
            return self_tw

    def screen_candidates(self, candidates, output = "mix"):
        if candidates is not None and len(candidates)>0:
            if output == "agent":
                candidates = [int(i) for i in candidates if str(i)[0]!="m"]
                #print("agent", candidates)
            if output == "media":
                candidates = [i for i in candidates if str(i)[0] =="m"]
                #print("media", candidates)
            if len(candidates)>0:
                target = np.random.choice(list(candidates))
                #print(target)
                if str(target)[0]!= "m":
                    target = int(target)
                return target

    
    def friend_repost(self, fri, output = "mix"): 
        if fri is not None:
            original_posters = set(fri.original_poster.values)- self.me_fri_subs
            candidate =  self.screen_candidates(original_posters, output= output)
            return candidate
        
    def friend_recommend(self, Message_db, output= "mix"):
        recent = Message_db[~Message_db.rt_poster.isin(self.me_fri_subs)].tail(21) ### hidden parameter
        #print("Recent message board", recent)
        if len(recent) >0:
            #recent["fri_or_foe"] = np.where(np.abs(recent.content.values-self.o) < self.eta, True, False)
            recommend = self.find_fri(recent) #recent[recent.fri_or_foe == True]
            if recommend is not None:
                if len(recommend) > 0:
                    candidate =  self.screen_candidates(recommend.rt_poster, output= output)
                    #print("candidate", candidate)
                    return candidate

    def friend_random(self, output = "mix"):
        non_friends = list(set(self.G.nodes).union(set(self.mids)) - self.me_fri_subs)
        candidate = self.screen_candidates(non_friends, output= output)
        #print("random", candidate)
        if candidate is None:
            if output == "media":
                return np.random.choice(self.mids) ### exception        
        else:
            return candidate

        
    def find_unfriend(self, foe):
        #if np.random.random()<self.p:
        if foe is not None:
            if len(foe)>0:
                target_foe = np.random.choice(foe["rt_poster"])
                return target_foe
    
    def find_friend(self, fri, Message_db, output, print_method =False):
        new_friend = None
        if fri is not None and len(fri) >0:
            new_friend = self.friend_repost(fri, output = output)
            method = "repost"
        if new_friend is None:
            new_friend = self.friend_recommend(Message_db, output = output)
            method = "recommend"
        if new_friend is None:
            new_friend = self.friend_random(output = output)
            method = "random"
        if new_friend is None:
            print(str(self.uid), "Warning: NOT finding a random/repost/recommend {}".format(output))
        elif print_method:
            print(self.uid, "found", new_friend, "through", method)
        if self.uid == new_friend:
            print(self.uid, "Self loop warning", method)
        return new_friend
                          
            
            


            
            

