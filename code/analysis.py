import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from sim import sim
#from Media import mass_media
import numpy as np, pandas as pd, json as js, csv
from tqdm import tqdm, tgrange
#from itertools import product

#
ROOT_DIR = "/N/slate/harryan/sim_data"

def getdir(N,s,eta):
    cwd = ROOT_DIR + f"N{str(N)}/s{str(s)[-1]}eta{str(eta)[-1]}" 
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        for i in ["Messages", "Opinions", "Networks", "Meta", "Effects", "Subscription"]:
            os.makedirs(cwd+ "/" + i)
    return cwd

para = np.arange(1, 10, 2)/10
paras = [(0.5, i) for i in para]

#for para in tqdm(para_list, desc= "Run"):
    #c, p, s = para
    #media_para, 
rep = 100
N = 3

class NumpyEncoder(js.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return js.JSONEncoder.default(self, obj)


for s, eta in paras:
    cwd = getdir(N, s, eta)
    for i in tqdm(range(rep), desc= f"Rep p{str(eta)} s{str(s)}"):
        lab = str(i)
        sm, md = sim(s, N, eta, include_media = True, effect_record= True) 
        with open(cwd + "/Meta/screen_size.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(sm.l)
       # with open(cwd + "/Meta/config.txt", "a") as f:
            #js.dump({i: sm.Config_db}, f)
            #f.write("\n")
        sm.Message_db.original_poster = sm.Message_db.original_poster.astype(str)
        sm.Message_db.rt_poster = sm.Message_db.rt_poster.astype(str)
        sm.Message_db.to_parquet(cwd + "/Messages/"+ lab + ".parquet")
        pd.DataFrame(sm.Opinions_db).to_parquet(cwd + "/Opinions/"+ lab + ".parquet")
        sm.ME_db.to_parquet(cwd + "/Effects/"+ lab + ".parquet")
        with open(cwd + "/Subscription/"+lab + ".json", "a") as f:
            js.dump(md.Subs_db, f, cls=NumpyEncoder)
        with open(cwd + "/Networks/{}.json".format(lab), "w") as f:
                js.dump(sm.Network_db, f)

