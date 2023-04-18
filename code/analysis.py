from sim import sim
#from Media import mass_media
import os, numpy as np, pandas as pd, json as js, csv
from tqdm import tqdm, tgrange
from itertools import permutations

#
ROOT_DIR = "/Users/harryan/Desktop/sim_data/"
def set_para(N, p, s):
    #media_para = {1:{"N":N, "p": p, "s":s, "id":"N{}p0{}s0{}".format(str(N)[-1], str(p)[-1], str(s)[-1]) }}
              #2:{"c":.5, "p": .1, "s": .5,"id":"con_media" }    }  #<-----------
    cwd = os.getcwd() + "/" + media_para[1]["id"]
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        for i in ["Messages", "Opinions", "Networks", "Meta", "Effects"]:
            os.makedirs(cwd+ "/" + i)
    return cwd

#paras = list(permutations(np.arange(1, 10, 2)/10, 2))

#for para in tqdm(para_list, desc= "Run"):
    #c, p, s = para
    #media_para, 
rep = 100
N = 1
p = 1
s = 1

media_para, cwd = set_para(N,p,s) 
for i in tqdm(range(rep), desc= "Repitition"):
    lab = str(i)
    sm, md = sim(p, s, N, 
        include_media = False, effect_record= True) ## Baseline
    with open(cwd + "/Meta/screen_size.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(sm.l)
    with open(cwd + "/Meta/config.txt", "a") as f:
        js.dump({i: sm.Config_db}, f)
        f.write("\n")
    sm.Message_db.to_parquet(cwd + "/Messages/"+ lab + ".parquet")
    pd.DataFrame(sm.Opinions_db).to_parquet(cwd + "/Opinions/"+ lab + ".parquet")
    sm.ME_db.to_parquet(cwd + "/Effects/"+ lab + ".parquet")
    with open(cwd + "/Networks/{}.json".format(lab), "w") as f:
            js.dump(sm.Network_db, f)
            #print("Progress: {}%".format(str(i)))
#vis(sm, "+/-.5", ".1", ".5", "balance_media")

