import os, argparse
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from entropies_TS import entropies_folder
import pandas as pd

ROOT_DIR = "/N/slate/harryan/sim_data/"
TAR_DIR = "/N/slate/harryan/sim_data_extra/"
#os.mkdir(TAR_DIR+"individual")

Ns = ["N" + str(i) for i in range(0,6)]
data_folders = []
for n in Ns:
    n_f = ROOT_DIR+f"{n}/"
    folders = os.listdir(n_f)
    for f in folders:
        data_folders.append(f"{n_f}{f}")


def run_entropies_ts(e, s):
    for folder in data_folders[e:s]:
        f = folder.split("/")[-2:]
        #for iteration in range(100):
        df_res = entropies_folder(folder, iterations = 100)
        df_res.to_parquet(TAR_DIR + f"/entropy_timeseris/{''.join(f)}.parquet")


if __name__ == '__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments for sim function
    parser.add_argument('s', type=int, help='Start')
    parser.add_argument('e', type=int, help='End')

    # Parse the command-line arguments
    args = parser.parse_args()
    res = run_entropies_ts(args.s, args.e)