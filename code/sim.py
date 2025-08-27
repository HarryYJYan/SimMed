"""Agent-based model simulation for studying mass media effects on opinion dynamics.

This module implements an agent-based model to study how mass media systems influence
opinion formation and polarization in social networks. The model is based on cultivation
theory and examines mainstreaming effects in high-choice media environments.

The simulation models:
- Social media platform with users connected in a network
- Mass media systems that can influence user opinions
- User behaviors including posting, following/unfollowing, and opinion updates
- Network dynamics with rewiring based on opinion similarity

References:
    This code implements the model described in the paper studying mass media effects
    using agent-based modeling and cultivation theory framework.
"""

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
    """Run agent-based simulation of media effects on opinion dynamics.
    
    This function simulates opinion formation and evolution in a social network
    with mass media influence. Users interact through social media, update their
    opinions based on social influence and media exposure, and can follow/unfollow
    others based on opinion similarity.
    
    Args:
        s (float): Audience share/reach parameter (0-1). Proportion of users exposed to media.
        N (int): Number of mass media systems in the simulation.
        eta (float): Tolerance threshold for opinion similarity (0-1). Users only interact
                    with others whose opinions are within this distance.
        p (float, optional): Media activity probability. Defaults to 0.5.
        mix (bool, optional): Allow cross-cutting exposure between social and mass media.
                             Defaults to False.
        include_media (bool, optional): Include mass media in simulation. Defaults to True.
        effect_record (bool, optional): Record media effects data. Defaults to True.
        n (int, optional): Number of users/agents in the network. Defaults to 100.
        m (int, optional): Number of edges in the initial network. Defaults to 400.
        T (int, optional): Number of time steps to simulate. Defaults to 10000.
        miu (float, optional): Strength of social influence (0-1). Defaults to 0.3.
        prob_rewire (float, optional): Probability of network rewiring at each step.
                                      Defaults to 0.3.
        rand (float, optional): Noise level in opinion updates. Defaults to 0.2.
    
    Returns:
        tuple: A tuple containing:
            - sm (SocialMedia): Social media platform object with simulation results
            - md (MassMedia): Mass media system object with subscription data
    
    Example:
        >>> # Run simulation with 3 media systems, 50% audience reach, tolerance=0.4
        >>> social_media, mass_media = sim(s=0.5, N=3, eta=0.4)
        >>> 
        >>> # Access final opinion distribution
        >>> final_opinions = social_media.O
        >>> 
        >>> # Get opinion evolution over time
        >>> opinion_history = social_media.Opinions_db
    """
    # Initialize social media platform and mass media systems
    sm = SocialMedia(n= n, m = m) 
    md = MassMedia(p, s, N)
    
    # Main simulation loop
    for t in np.arange(T):#tqdm(np.arange(T), desc = "Run: "): #np.arange(T):
        # Get current opinion state
        Os = sm.Opinions_db[list(sm.Opinions_db.keys())[-1]]
        
        # Mass media posts messages based on audience opinions
        send_media_message(sm, md, Os, include_media)
        
        # Sample a random user for this time step
        uid, l = sample_user(sm)
        if uid is not None:
            # Get user's media subscriptions
            subs = md.find_subs(uid)
            
            # Simulate user activity: opinion update, posting, social interactions
            user, fri, foe, new_o, new_post = user_activity(uid, sm, md, eta, miu, l, subs, rand, include_media)
            
            # Record user's new message
            sm.add_message(new_post)
            
            # Update user's opinion in the database
            sm.update_Opinions_db(uid, new_o, t)
            
            # Record media effects if tracking is enabled
            if effect_record == True:
                sm.update_ME_db(t, uid, fri, foe)
            
            # Update network structure based on opinion similarity
            update_network(user, prob_rewire, fri, foe, md, sm, mix = mix)
            
            # Record network and subscription changes
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

