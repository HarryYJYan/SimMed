import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import pandas as pd
from entropy_continuous import entropy_continuous


#ROOT_DIR = "/N/slate/harryan/sim_data/"

def entropies_folder(folder, iterations =100):
    time_index = [f"Time_{str(i)}" for i in range(10000)]
    entropies =[]
    for iteration in range(iterations):
        f_dir = f"{folder}/opinions/{str(iteration)}_opinions.parquet"
        #print(f_dir)
        op = pd.read_parquet(f_dir)
        entropy_one_iter = op.apply(entropy_continuous, axis = 0)
        one_iter_reindex = entropy_one_iter.reindex(time_index, fill_value= np.nan)
        one_iter_fillna = one_iter_reindex.fillna((one_iter_reindex.ffill() + one_iter_reindex.bfill()) / 2)
        entropies.append(one_iter_fillna)
    entropies_df = pd.concat(entropies, axis = 1)
    return entropies_df
