import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import pandas as pd
import networkx as nx
import json as js

def n_cpnts_folder(folder, iterations =100):
    time_index = [f"Time_{str(i)}" for i in range(10000)]
    n_folder =[]
    for iteration in range(iterations):
        f_dir = f"{folder}/networks/{str(iteration)}_networks.json"
        #print(f_dir)
        with open(f_dir, 'r') as f:
            networks =  js.load(f)
        n_iter = {}
        for timestep, edgelist in networks.items():
            g_t = nx.from_edgelist(edgelist, create_using= nx.Graph)
            n_t = nx.number_connected_components(g_t)
            n_iter[timestep] = n_t
        n_iter = pd.Series(n_iter)
        n_iter = n_iter.reindex(time_index, fill_value= np.nan)
        n_iter = n_iter.fillna(n_iter.ffill())
        n_folder.append(n_iter)
    n_df = pd.concat(n_folder, axis = 1)
    return n_df