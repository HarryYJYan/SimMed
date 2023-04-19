from sim import sim
#from Media import mass_media
import os, numpy as np, pandas as pd, json as js, csv
from tqdm import tqdm, tgrange


ROOT_DIR = "/Users/harryan/Desktop/sim_data/baseline/"

def getdir(rep):
    cwd = ROOT_DIR + f"{str(rep)}" 
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        for i in ["Messages", "Opinions", "Networks", "Meta", "Effects"]:
            os.makedirs(cwd+ "/" + i)
    return cwd



REP = 100
 
for i in tqdm(range(REP), desc= "Repitition"):
    lab = str(i)
    cwd = getdir(i)
    sm, md = sim(0, 0, 1, include_media = False, effect_record= True) ## Baseline
    with open(cwd + "/Meta/screen_size.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(sm.l)
    sm.Messege_db.to_parquet(cwd + "/Messages/"+ lab + ".parquet")
    pd.DataFrame(sm.Opinions_db).to_parquet(cwd + "/Opinions/"+ lab + ".parquet")
    sm.ME_db.to_parquet(cwd + "/Effects/"+ lab + ".parquet")
    with open(cwd + "/Networks/{}.json".format(lab), "w") as f:
            js.dump(sm.Network_db, f)



