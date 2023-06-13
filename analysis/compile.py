import pandas as pd, os
from tqdm import tqdm

ROOT_DIR = "/N/slate/harryan/sim_data/"
TAR_DIR = "/N/slate/harryan/sim_data_extra/"

Ns = ["N"+str(i) for i in range(6)]
op_folders = []
for n in Ns:
    n_f = ROOT_DIR+f"{n}/"
    folders = os.listdir(n_f)
    for f in folders:
        op_folders.append(f"{n}/{f}/opinions/")

def get_raw_op(folder, pos):
    PATHs = ROOT_DIR + folder
    files = os.listdir(PATHs)
    data =[]
    new_col = []
    for f in files:
        new_col.append(f.split("_")[0])
        df = pd.read_parquet(PATHs + f)
        data.append(df[df.columns[pos]])
    res = pd.concat(data, axis = 1)
    res.columns = new_col
    new_file_name = folder.replace("/","_")[:-1] + ".parquet"
    if pos == 0:
        res.to_parquet(TAR_DIR+"opinions_init/" + new_file_name)
    if pos == -1:
        res.to_parquet(TAR_DIR+"opinions/" + new_file_name) 

