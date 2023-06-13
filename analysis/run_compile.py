from compile import get_raw_op
from tqdm import tqdm
import os, argparse

ROOT_DIR = "/N/slate/harryan/sim_data/"
TAR_DIR = "/N/slate/harryan/sim_data_extra/"

Ns = ["N"+str(i) for i in range(6)]
op_folders = []
for n in Ns:
    n_f = ROOT_DIR+f"{n}/"
    folders = os.listdir(n_f)
    for f in folders:
        op_folders.append(f"{n}/{f}/opinions/")

def run_compile(s, e, pos):
    for folder in tqdm(op_folders[s:e]):
        get_raw_op(folder, pos)


if __name__ == '__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments for sim function
    parser.add_argument('s', type=int, help='Start')
    parser.add_argument('e', type=int, help='End')
    parser.add_argument('pos', type=int, help='Position')

    # Parse the command-line arguments
    args = parser.parse_args()
    res = run_compile(args.s, args.e, args.pos)