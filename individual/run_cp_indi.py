import os, argparse
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import sys
sys.path.append('/N/u/harryan/BigRed200/SimMed/individual')
from compile_indi import ind_diff_one
import pandas as pd

ROOT_DIR = "/N/slate/harryan/sim_data/"
TAR_DIR = "/N/slate/harryan/sim_data_extra/"
#os.mkdir(TAR_DIR+"individual")

Ns = ["N" + str(i) for i in range(1,6)]
data_folders = []
for n in Ns:
    n_f = ROOT_DIR+f"{n}/"
    folders = os.listdir(n_f)
    for f in folders:
        data_folders.append(f"{n_f}{f}")


ctv = {}

def run_cp_ind(e, s):
    for folder in data_folders[e:s]:
        f = folder.split("/")[-2:]
        for iteration in range(100):
            ctv[tuple(f+[iteration])] = ind_diff_one(folder, iteration)
        df_res =pd.DataFrame(ctv).T.reset_index()
        df_res.columns = ["N", "config", "iter", "exp_corr", "eff_corr"]
        df_res.to_csv(TAR_DIR + f"individual/{''.join(f)}.csv")


if __name__ == '__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments for sim function
    parser.add_argument('s', type=int, help='Start')
    parser.add_argument('e', type=int, help='End')

    # Parse the command-line arguments
    args = parser.parse_args()
    res = run_cp_ind(args.s, args.e)