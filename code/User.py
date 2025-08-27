"""User Module for Agent-Based Media Effects Simulation.

This module implements individual user behavior in the agent-based model
for studying media effects on opinion dynamics. Users interact with content,
update their opinions, form social connections, and generate content.

The User class represents individual agents that:
- Have opinions that can change based on social influence
- View content from their social network and media subscriptions
- Decide to follow/unfollow others based on opinion similarity
- Generate posts and reposts based on consumed content
- Are influenced by tolerance thresholds for opinion similarity

Classes:
    User: Individual user/agent in the simulation
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np, pandas as pd

class User():
    """Individual User Agent for Social Media Simulation.
    
    This class represents a single user in the social media simulation.
    Users have opinions, social connections, media subscriptions, and
    exhibit various behaviors like posting, following, and opinion updating.
    
    Attributes:
        uid (int): Unique user identifier
        eta (float): Tolerance threshold for opinion similarity
        miu (float): Strength of social influence on opinion updates
        o (float): Current opinion value (-1 to 1)
        G (networkx.DiGraph): Social network graph
        f (networkx view): Users that this user follows
        subs (list): Media subscriptions
        mids (list): Available media system IDs
        me_fri_subs (set): Combined set of self, friends, and subscriptions
    """
    def __init__(self, uid, eta, miu, o, G, subs, mids):
        """Initialize a user agent.
        
        Args:
            uid (int): Unique user identifier
            eta (float): Tolerance threshold for opinion similarity (0-1)
            miu (float): Strength of social influence (0-1)
            o (float): Initial opinion value (-1 to 1)
            G (networkx.DiGraph): Social network graph
            subs (list): Current media subscriptions
            mids (list): Available media system IDs
        """
        self.uid = uid
        self.eta = eta    # Tolerance threshold
        self.miu = miu    # Social influence strength
        self.o = o        # Current opinion
        self.G = G        # Network graph
        self.f = self.G.successors(uid)  # Users this user follows
        self.subs = subs  # Media subscriptions
        self.mids = mids  # Available media systems
        
        # Combined set for filtering (self + friends + subscriptions)
        self.me_fri_subs = set(self.f).union({self.uid}).union(self.subs)


    def find_fri(self, screen):
        """Identify messages from similar-minded users/media (friends).
        
        Messages are considered 'friendly' if their content is within the
        user's tolerance threshold of their current opinion.
        
        Args:
            screen (pd.DataFrame or None): Messages visible to the user
            
        Returns:
            pd.DataFrame or None: Messages from similar-minded sources
        """
        if screen is not None:
            # Calculate opinion similarity
            screen["fri_or_foe"] = np.where(
                np.abs(screen.content.values - self.o) < self.eta, 
                True, False
            )
            fri = screen[screen.fri_or_foe == True]
            if len(fri) > 0:
                return fri
            else:
                return None
    
    def find_foe(self, screen):
        """Identify messages from dissimilar users/media (foes).
        
        Messages are considered 'hostile' if their content is outside the
        user's tolerance threshold of their current opinion.
        
        Args:
            screen (pd.DataFrame or None): Messages visible to the user
            
        Returns:
            pd.DataFrame or None: Messages from dissimilar sources
        """
        if screen is not None:
            # Calculate opinion dissimilarity
            screen["fri_or_foe"] = np.where(
                np.abs(screen.content.values - self.o) < self.eta, 
                True, False
            )
            foe = screen[screen.fri_or_foe == False]
            if len(foe) > 0:
                return foe
            else:
                return None
 
    def update_opinion(self, fri, rand):
        """Update user's opinion based on social influence and noise.
        
        Opinion change is based on the average opinion difference from
        friendly messages, scaled by social influence strength, plus noise.
        
        Args:
            fri (pd.DataFrame or None): Messages from similar-minded sources
            rand (float): Noise level in opinion updates
            
        Returns:
            float or None: New opinion value, or None if no update
        """
        if fri is not None:
            # Calculate social influence from friendly messages
            social_influence = self.miu * np.mean(fri.content - self.o)
            
            # Add random noise
            noise = (np.random.random() * 2 - 1) * rand
            
            # Calculate new opinion
            new_opinion = self.o + social_influence + noise
            
            return new_opinion

    def generate_post(self, fri, p=0.5):
        """Generate a post or repost based on consumed content.
        
        With probability p, the user reposts a friendly message.
        Otherwise, they create an original post expressing their opinion.
        
        Args:
            fri (pd.DataFrame or None): Messages from similar-minded sources
            p (float, optional): Probability of reposting. Defaults to 0.5.
            
        Returns:
            pd.DataFrame: Generated message data
        """
        if np.random.random() < p:
            if fri is not None:
                # Repost a friendly message
                rt = fri.sample(1)
                rt["rt_poster"] = self.uid
                rt["rt_status"] = True
                rt.drop(["fri_or_foe"], axis=1, inplace=True)
                return rt    
        else:
            # Create original post with current opinion
            self_tw = pd.DataFrame({
                "original_poster": [self.uid], 
                "rt_poster": [self.uid], 
                "content": [self.o], 
                "rt_status": [False]
            })
            return self_tw

    def screen_candidates(self, candidates, output="mix"):
        """Filter and select from candidate users/media for following.
        
        Args:
            candidates (iterable or None): Potential targets to follow
            output (str, optional): Type filter - 'agent', 'media', or 'mix'. 
                                  Defaults to 'mix'.
                                  
        Returns:
            int or str or None: Selected target ID, or None if no candidates
        """
        if candidates is not None and len(candidates) > 0:
            if output == "agent":
                # Filter for user agents only (no media)
                candidates = [int(i) for i in candidates if str(i)[0] != "m"]
            elif output == "media":
                # Filter for media systems only
                candidates = [i for i in candidates if str(i)[0] == "m"]
            
            if len(candidates) > 0:
                target = np.random.choice(list(candidates))
                # Convert to int if it's a user agent
                if str(target)[0] != "m":
                    target = int(target)
                return target

    
    def friend_repost(self, fri, output="mix"): 
        """Find new connections from original posters of friendly messages.
        
        Looks at who originally posted the friendly content and considers
        following them if not already connected.
        
        Args:
            fri (pd.DataFrame or None): Friendly messages
            output (str, optional): Type filter. Defaults to 'mix'.
            
        Returns:
            int or str or None: Selected target to follow
        """
        if fri is not None:
            # Get original posters excluding already connected users
            original_posters = set(fri.original_poster.values) - self.me_fri_subs
            candidate = self.screen_candidates(original_posters, output=output)
            return candidate
        
    def friend_recommend(self, Message_db, output="mix"):
        """Find new connections from recent friendly messages.
        
        Looks at recent messages from non-connected users and considers
        following those with similar opinions.
        
        Args:
            Message_db (pd.DataFrame): All messages on the platform
            output (str, optional): Type filter. Defaults to 'mix'.
            
        Returns:
            int or str or None: Selected target to follow
        """
        # Get recent messages from non-connected users (last 21 messages)
        recent = Message_db[~Message_db.rt_poster.isin(self.me_fri_subs)].tail(21)
        
        if len(recent) > 0:
            # Find friendly messages among recent posts
            recommend = self.find_fri(recent)
            if recommend is not None and len(recommend) > 0:
                candidate = self.screen_candidates(recommend.rt_poster, output=output)
                return candidate

    def friend_random(self, output="mix"):
        """Randomly select a new connection from all available users/media.
        
        Fallback method when targeted approaches don't find candidates.
        
        Args:
            output (str, optional): Type filter. Defaults to 'mix'.
            
        Returns:
            int or str or None: Selected target to follow
        """
        # Get all non-connected users and media
        non_friends = list(set(self.G.nodes).union(set(self.mids)) - self.me_fri_subs)
        candidate = self.screen_candidates(non_friends, output=output)
        
        # Fallback for media-only selection if no candidates found
        if candidate is None and output == "media":
            return np.random.choice(self.mids)
        else:
            return candidate

        
    def find_unfriend(self, foe):
        """Select a target to unfollow from hostile message sources.
        
        Randomly selects from users/media who posted or reposted
        content that conflicts with the user's opinion.
        
        Args:
            foe (pd.DataFrame or None): Hostile/dissimilar messages
            
        Returns:
            int or str or None: Target to unfollow
        """
        if foe is not None and len(foe) > 0:
            target_foe = np.random.choice(foe["rt_poster"])
            return target_foe
    
    def find_friend(self, fri, Message_db, output, print_method=False):
        """Find a new user/media to follow using multiple strategies.
        
        Tries three methods in order:
        1. Follow original posters of friendly content (repost method)
        2. Follow recent posters of similar opinions (recommend method)
        3. Random selection from available targets (random method)
        
        Args:
            fri (pd.DataFrame or None): Friendly messages
            Message_db (pd.DataFrame): All platform messages
            output (str): Type filter - 'agent', 'media', or 'mix'
            print_method (bool, optional): Print debugging info. Defaults to False.
            
        Returns:
            int or str or None: Selected target to follow
        """
        new_friend = None
        method = None
        
        # Strategy 1: Follow original posters of friendly content
        if fri is not None and len(fri) > 0:
            new_friend = self.friend_repost(fri, output=output)
            method = "repost"
            
        # Strategy 2: Follow recent similar-minded posters
        if new_friend is None:
            new_friend = self.friend_recommend(Message_db, output=output)
            method = "recommend"
            
        # Strategy 3: Random selection
        if new_friend is None:
            new_friend = self.friend_random(output=output)
            method = "random"
            
        # Error checking and debugging
        if new_friend is None:
            print(str(self.uid), "Warning: NOT finding a random/repost/recommend {}".format(output))
        elif print_method:
            print(self.uid, "found", new_friend, "through", method)
            
        if self.uid == new_friend:
            print(self.uid, "Self loop warning", method)
            
        return new_friend
                          
            
            


            
            

