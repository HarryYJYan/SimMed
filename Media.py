import numpy as np, pandas as pd

class MassMedia():
    def __init__(self, c, p,  s,id, n=100):
        self.c = c
        self.p = p
        self.id = id
        self.audience = np.random.choice(np.arange(n), int(np.floor(n*s)), replace = False).tolist()
        #self.meta = {"c{}p{}s{}".format(str(c).strip("."), str(p).strip("."), str(s).strip(".")): self.audience}
        
    def media_message(self, d = .25):
        #d = .3
        if np.random.rand() < self.p:
            v = self.c + d*(np.random.rand()*2 -1)
            post = pd.DataFrame({"original_poster": [self.id], "rt_poster": [self.id], "content": [v], "rt_status":[False]})
            return post
        else:
            return None
#MassMedia(0, .5, .6,  "test", 100 ).audience

