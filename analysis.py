from sim import sim
#from Media import mass_media
import os, numpy as np, pandas as pd, json as js, csv
from tqdm import tqdm, tgrange
from itertools import permutations
#from vis import vis
#eta = .5
#miu = .3
#q  = .3
#T = 10000
#rand = .25
#n = 100
#m = 400

def set_para(c, p, s):
    media_para = {1:{"c":c, "p": p, "s":s, "id":"c0{}p0{}s0{}".format(str(c)[-1], str(p)[-1], str(s)[-1]) }}
              #2:{"c":.5, "p": .1, "s": .5,"id":"con_media" }    }  #<-----------
    cwd = os.getcwd() + "/" + media_para[1]["id"]
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        for i in ["Messages", "Opinions", "Networks", "Meta", "Effects"]:
            os.makedirs(cwd+ "/" + i)
    return media_para, cwd

#paras = list(permutations(np.arange(1, 10, 2)/10, 2))

#for para in tqdm(para_list, desc= "Run"):
    #c, p, s = para
    #media_para, 
rep = 5
c = 0
p = 0
s = 0
media_para, cwd = set_para(c,p,s) 
for i in tqdm(range(rep), desc= "Rep"):
    lab = str(i)
    sm = sim(media_para = media_para,
        include_media = False, effect_record= True) ## Baseline
    with open(cwd + "/Meta/screen_size.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(sm.l)
    with open(cwd + "/Meta/config.txt", "a") as f:
        js.dump({i: sm.Config_db}, f)
        f.write("\n")
    sm.Message_db.to_csv(cwd + "/Messages/"+ lab + ".csv")
    pd.DataFrame(sm.Opinions_db).to_csv(cwd + "/Opinions/"+ lab + ".csv")
    sm.ME_db.to_csv(cwd + "/Effects/"+ lab + ".csv")
    with open(cwd + "/Networks/{}.json".format(lab), "w") as f:
            js.dump(sm.Network_db, f)
            #print("Progress: {}%".format(str(i)))
#vis(sm, "+/-.5", ".1", ".5", "balance_media")

