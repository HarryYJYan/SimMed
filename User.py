import numpy as np, pandas as pd

class User():
    def __init__ (self, uid, eta, miu, o, G, media_dict):
        self.uid = uid
        #self.p = .5
        #self.q = q
        self.eta = eta
        self.miu= miu
        #self.screen = screen
        self.o = o
        self.G = G
        self.f = self.G.successors(uid) 
        self.media_ids = list(media_dict.keys()) #["mainstream_media", "liberal_media", "conservative_media", "extreme_liberal_media", "extreme_conservative_media"]
        self.sub = [v.id for k, v in media_dict.items() if uid in v.audience]


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
    
    def friend_random(self):
        #print(me_and_friends) 
        #if np.random.random()< self.p:
        me_and_friends = set(self.f).union({self.uid})#.union(self.media_id)
        non_friends = set(self.G.nodes) - me_and_friends
        target = int(np.random.choice(list(non_friends)))
        self.G.add_edge(self.uid, target)
        return True
    
    def friend_repost(self,screen): #fri):
        #f = copy.copy(self.f)
        #if np.random.random()< self.p:
        if screen is not None:
            me_and_friends_media = set(self.f).union({self.uid}).union(self.media_ids)
            original_posters = set(screen.original_poster.values)- me_and_friends_media
            if len(original_posters) >0:
                target = int(np.random.choice(list(original_posters)))
                self.G.add_edge(self.uid, target)
                return True
        
    def friend_recommend(self, recommend):
        #if np.random.random() < self.p:
        if recommend is not None:
            target = int(recommend.rt_poster.sample(1))
            #print("Agent {} followed {}".format(str(self.uid, target)))
            self.G.add_edge(self.uid, target)
            return True
        
    def unfriend(self, foe):
        #if np.random.random()<self.p:
        if foe is not None:
            foe = foe[~foe["rt_poster"].isin(self.media_ids)]
            if len(foe)>0:
                target_foe = int(foe["rt_poster"].sample(1))
                #print("Agent {} unfollowed {}".format(str(self.uid, target_foe)))
                self.G.remove_edge(self.uid, target_foe)
                self.f = self.G.successors(self.uid) 
                #print("Deleted ({},{})".format(str(self.uid),str(target_foe)))
                return True
            
            


            
            

