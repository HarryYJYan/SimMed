"""Mass Media Module for Agent-Based Media Effects Simulation.

This module implements the mass media component of the agent-based model
for studying media effects on opinion dynamics. It manages multiple media
systems, their audiences, and content generation based on audience opinions.

The MassMedia class represents media systems that:
- Have different audience shares and subscriber bases
- Generate content based on their audience's average opinion
- Can be subscribed to and unsubscribed from by users
- Influence opinion formation through message posting

Classes:
    MassMedia: Main mass media systems manager
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np, pandas as pd
import copy

class MassMedia():
    """Mass Media Systems for Agent-Based Simulation.
    
    This class manages multiple mass media systems that can influence user
    opinions through content generation. Each media system has its own
    audience and generates content based on the average opinion of its
    subscribers.
    
    Attributes:
        p (float): Media activity probability
        s (float): Audience share parameter (proportion of users exposed)
        n (int): Number of media systems
        agents (int): Total number of users in the simulation
        mids (list): Media system identifiers
        shares (list): Market share of each media system
        init_subs (list): Initial subscriber lists for each media
        subs (dict): Current subscriber mapping {media_id: [user_ids]}
        Subs_db (dict): Historical subscription data
    """
    def __init__(self, p, s, n, agents = 100):
        """Initialize mass media systems.
        
        Args:
            p (float): Media activity probability (0-1)
            s (float): Audience share parameter (0-1)
            n (int): Number of media systems
            agents (int, optional): Total number of users. Defaults to 100.
        """
        self.p = p          # Media activity probability
        self.s = s          # Audience share parameter
        self.n = n          # Number of media systems
        self.agents = agents # Total number of users
        
        # Create media system identifiers
        self.mids = ["m"+str(i) for i in range(n)]
        
        # Initialize market shares and subscriber base
        self.shares = self.init_share()
        self.init_subs = self.split_list()
        self.subs = {self.mids[i]: self.init_subs[i] for i in range(n)}
        
        # Initialize subscription tracking
        self.Subs_db = {"Time_0": copy.deepcopy(self.subs)}
        
    def init_share(self):
        """Initialize market share for each media system.
        
        Randomly divides the total audience among media systems to determine
        the relative market share of each system.
        
        Returns:
            list: Market share (number of potential subscribers) for each media system
        """
        holders = np.ones(self.agents)
        splits = np.random.choice(np.arange(1, self.agents), self.n-1, replace=False)
        splits = [0] + list(sorted(splits)) + [self.agents]
        res = [int(np.sum(holders[splits[i]:splits[i+1]])) for i in range(self.n)]
        return res 
    
    def split_list(self):
        """Create initial subscriber lists for each media system.
        
        Assigns users to media systems based on market share and audience
        reach parameter. Creates non-overlapping subscriber groups.
        
        Returns:
            list: List of subscriber lists for each media system
        """
        start = 0
        end = 0
        output = []
        
        # Calculate total audience size based on reach parameter
        aud_size = int(np.ceil(self.agents * self.s))
        aud_ids = np.random.choice(np.arange(self.agents), aud_size, replace=False)
        
        # Calculate subscriber count for each media based on market share
        sizes = np.int32(np.ceil(np.array(self.shares) * self.s))
        
        # Distribute subscribers among media systems
        for size in sizes:
            end += size
            output.append(aud_ids[start:end].tolist())
            start = end
            
        return output
    
    def random_split(self):
        """Alternative method: Create overlapping subscriber lists.
        
        This method allows users to subscribe to multiple media systems,
        creating potential overlap in audiences.
        
        Returns:
            list: List of subscriber lists for each media system (with possible overlap)
        """
        aud_size = int(np.ceil(self.agents * self.s))
        aud_ids = np.random.choice(np.arange(self.agents), aud_size, replace=False)
        sizes = np.int32(np.ceil(np.array(self.shares) * self.s))
        return [np.random.choice(aud_ids, size, replace=False) for size in sizes]
    
    def media_message(self, mid, Os, d = .25):
        """Generate a media message based on audience opinion.
        
        Each media system generates content that reflects the average opinion
        of its current subscribers, with some random noise added.
        
        Args:
            mid (str): Media system identifier
            Os (np.ndarray): Current opinion state of all users
            d (float, optional): Noise parameter for content generation. Defaults to 0.25.
            
        Returns:
            pd.DataFrame or None: Message data if generated, None otherwise
        """
        if np.random.rand() < self.p:
            # Get current subscribers
            recent = self.Subs_db[list(self.Subs_db.keys())[-1]]
            
            # Calculate content based on subscriber opinions + noise
            v = np.mean(Os[recent[mid]]) + d * (np.random.rand() * 2 - 1)
            
            # Create message
            post = pd.DataFrame({
                "original_poster": [mid], 
                "rt_poster": [mid], 
                "content": [v], 
                "rt_status": [False]
            })
            return post
        else:
            return None
    
    def find_subs(self, uid):
        """Find which media systems a user subscribes to.
        
        Args:
            uid (int): User ID
            
        Returns:
            list: List of media system IDs that the user subscribes to
        """
        subs = [k for k, v in self.subs.items() if uid in v]
        return subs
        
    def cancel(self, uid, foe_target):
        """Cancel user's subscription to a media system.
        
        Args:
            uid (int): User ID
            foe_target (str): Media system ID to unsubscribe from
        """
        self.subs[foe_target].remove(uid)
    
    def subscribe(self, uid, fri_target):
        """Subscribe user to a media system.
        
        Args:
            uid (int): User ID  
            fri_target (str): Media system ID to subscribe to
        """
        if uid not in self.subs[fri_target]:
            self.subs[fri_target].append(uid)

    def update_Sub_DB(self, t):
        """Record current subscription state.
        
        Args:
            t (int): Current time step
        """
        self.Subs_db["Time_{}".format(t)] = copy.deepcopy(self.subs)


        


        


        

