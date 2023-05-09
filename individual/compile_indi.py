import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import pandas as pd

def ind_diff_one(folder, iteration):
    op = pd.read_parquet(f"{folder}/opinions/{str(iteration)}_opinions.parquet")
    start = op[op.columns[0]]
    end = op[op.columns[-1]]
    diff = np.abs(end - start)
    ms = pd.read_parquet(f"{folder}/messages/{str(iteration)}_messages.parquet")
    ef = pd.read_parquet(f"{folder}/effects/{str(iteration)}_effects.parquet")
    history = pd.merge(ms.reset_index(), ef, on = "index", how = "right")
    history["med_exp"] = history.original_poster.str.contains("m")
    history["med_eff"] = history.original_poster.str.contains("m") & history.effects == True
    exp = pd.DataFrame(history.groupby("uid").med_exp.value_counts(normalize= False).loc[slice(None), True])
    eff = pd.DataFrame(history.groupby("uid").med_eff.value_counts(normalize= False).loc[slice(None), True])
    res = pd.concat([diff, exp, eff], axis = 1).dropna().corr()[0].values[1:]
    return res