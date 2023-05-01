import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import pandas as pd, json as js
from sim import sim
import argparse

ROOT_DIR = "/N/slate/harryan/sim_data"
def run(s, N, eta, rep): #**kargs
    cwd = ROOT_DIR + f"/N{str(N)}/s{str(s)[-1]}eta{str(eta)[-1]}/" 
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        for folder in ["messages", "opinions", "networks", "effects", "screensizes", "subscriptions"]:
            os.makedirs(cwd+ folder)
    for iteration in range(rep):
        if N != 0:
            sm, md = sim(s, N, eta)
        else:
            sm, md = sim(s, 1, eta, include_media= False)#kargs
        opinions = pd.DataFrame(sm.Opinions_db)
        opinions.to_parquet(f"{cwd}/opinions/{str(iteration)}_opinions.parquet")
        ##
        messages = sm.Message_db
        messages.original_poster = messages.original_poster.astype(str)
        messages.rt_poster = messages.rt_poster.astype(str)
        messages.to_parquet(f"{cwd}/messages/{str(iteration)}_messages.parquet")
        ##
        with open(f"{cwd}/networks/{str(iteration)}_networks.json", "w") as f:
            js.dump(sm.Network_db, f) 
        ##
        effects = sm.ME_db 
        effects.to_parquet(f"{cwd}/effects/{str(iteration)}_effects.parquet")
        ##
        if N !=0:
            with open(f"{cwd}/screensizes/{str(iteration)}_screensizes.json", "w") as f:
                js.dump([int(x) for x in sm.l], f)
        ##
            with open(f"{cwd}/subscriptions/{str(iteration)}_subscriptions.json", "w") as f:
                js.dump(md.Subs_db, f)
    #return opinions, messages, networks, effects, screensizes, subscriptions
    
if __name__ == '__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments for sim function
    parser.add_argument('s', type=float, help='Share')
    parser.add_argument('N', type=int, help='Number of media')
    parser.add_argument('eta', type=float, help='Tolerence level')
    parser.add_argument('rep', type=int, help='Repition')

    # Parse the command-line arguments
    args = parser.parse_args()
    res = run(args.s, args.N, args.eta, args.rep)
