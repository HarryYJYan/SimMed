import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np#, pandas as pd, json as js
from SocialMedia import SocialMedia
from Media import MassMedia
from tqdm import tqdm
from activity import send_media_message, sample_user, user_activity, update_network
import argparse
          
def sim(s, N, eta,
        p =.5,
        mix = False, 
        include_media = True,
        effect_record = True, 
        n = 100, m = 400, 
        T = 10000, 
        miu = .3, 
        prob_rewire = .3, 
        rand =.2):  #rand,
    sm = SocialMedia(n= n, m = m) 
    md = MassMedia(p, s, N)
    for t in np.arange(T):#tqdm(np.arange(T), desc = "Run: "): #np.arange(T):
        Os = sm.Opinions_db[list(sm.Opinions_db.keys())[-1]]
        send_media_message(sm, md, Os, include_media)
        uid, l = sample_user(sm)
        if uid is not None:
            #print(uid, l)
            subs = md.find_subs(uid)
            user, fri, foe, new_o, new_post = user_activity(uid, sm, md, eta, miu, l, subs, rand, include_media)
            sm.add_message(new_post)
            sm.update_Opinions_db(uid, new_o, t)
            if effect_record == True:
                sm.update_ME_db(t, uid, fri, foe)
            update_network(user, prob_rewire, fri, foe, md, sm, mix = mix)
            sm.update_Network_db(t)
            md.update_Sub_DB(t)
    return sm, md

if __name__ == '__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments for sim function
    parser.add_argument('s', type=float, help='Share')
    parser.add_argument('N', type=int, help='Number of media')
    parser.add_argument('eta', type=float, help='Tolerence level')
    #parser.add_argument('iteration', type=int, help='iteration')
    parser.add_argument('--p', type=float, default=.5, help='activity')
    parser.add_argument('--mix', action='store_true', help='Allow cross-cutting exposure')
    parser.add_argument('--no-media', dest='include_media', action='store_false', help='Exclude include_media parameter')
    parser.add_argument('--no-effect', dest='effect_record', action='store_false', help='Exclude effect_record parameter')
    parser.add_argument('--n', type=int, default=100, help='Number of nodes')
    parser.add_argument('--m', type=int, default=400, help='Number of links')
    parser.add_argument('--T', type=int, default=10000, help='Time steps')
    parser.add_argument('--miu', type=float, default=.3, help='Social influence magnitutde')
    parser.add_argument('--prob-rewire', type=float, default=.3, help='Probability to rewire')
    parser.add_argument('--rand', type=float, default=.2, help='Noise level')

    # Parse the command-line arguments
    args = parser.parse_args()
    sm, md = sim(args.s, args.N, args.eta,
        p=args.p, 
        mix=args.mix, 
        include_media=args.include_media, 
        effect_record=args.effect_record, 
        n=args.n, m=args.m, 
        T=args.T, 
        miu=args.miu, 
        prob_rewire=args.prob_rewire, 
        rand=args.rand)

    #python sim.py <value for s> <value for N> <value for eta> --p <value for p> --mix --no-media --no-effect --n <value for n> --m <value for m> --T <value for T> --miu <value for miu> --prob-rewire <value for prob_rewire> --rand <value for rand>

