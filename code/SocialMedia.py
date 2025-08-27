"""Social Media Platform Module for Agent-Based Media Effects Simulation.

This module implements the social media platform component of the agent-based model
for studying mass media effects on opinion dynamics. It manages user networks,
message flows, and opinion evolution over time.

The SocialMedia class represents a social media platform where:
- Users are connected in a directed network
- Users have opinions that evolve over time
- Users post and repost messages
- Network structure changes based on opinion similarity
- All activities are tracked for analysis

Classes:
    SocialMedia: Main social media platform class
    
Functions:
    constrained_sum_sample_pos: Generate degree sequence for network
    random_graph_revised: Create random directed graph with given degree sequence
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import random
import networkx as nx, numpy as np, pandas as pd
import copy

def constrained_sum_sample_pos(n, m):
    """Generate a random sequence of positive integers that sum to m.
    
    This function creates a degree sequence for network generation by
    randomly partitioning the total number of edges among nodes.
    
    Args:
        n (int): Number of integers in the sequence (number of nodes)
        m (int): Target sum (total number of edges)
        
    Returns:
        list: List of n positive integers that sum to m
        
    Example:
        >>> sequence = constrained_sum_sample_pos(5, 20)
        >>> len(sequence)
        5
        >>> sum(sequence)
        20
    """
    dividers = sorted(random.sample(range(1, m), n - 1))
    return [a - b for a, b in zip(dividers + [m], [0] + dividers)]

def random_graph_revised(n, m):
    """Create a random directed graph with specified number of nodes and edges.
    
    This function generates a random directed network where each node has
    a randomly assigned out-degree, but the total number of edges is fixed.
    Used to create the initial social network structure.
    
    Args:
        n (int): Number of nodes in the graph
        m (int): Total number of directed edges
        
    Returns:
        networkx.DiGraph: Random directed graph with n nodes and m edges
        
    Example:
        >>> G = random_graph_revised(100, 400)
        >>> G.number_of_nodes()
        100
        >>> G.number_of_edges()
        400
    """
    degree_squence = constrained_sum_sample_pos(n, m)
    node_ids = list(range(n))
    edge_list = []
    for i in node_ids:
        non_self = [j for j in node_ids if i!= j]
        targets = random.sample(non_self, degree_squence[i]) 
        edges_of_n = [(i,target) for target in targets]
        edge_list = edge_list+ edges_of_n
    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    return G

#G = random_graph_revised(n, m)

class SocialMedia:
    """Social Media Platform for Agent-Based Simulation.
    
    This class represents a social media platform where users are connected
    in a network, share opinions, post messages, and interact with each other
    and mass media. The platform tracks all user activities and network changes
    over time for analysis.
    
    Attributes:
        p (float): Default activity probability
        n (int): Number of users in the network
        m (int): Number of edges in the network
        l (np.ndarray): Screen sizes for each user (activity levels)
        G (networkx.DiGraph): User network graph
        O (np.ndarray): Current opinions of all users
        Opinions_db (dict): Historical opinion data for all time steps
        Message_db (pd.DataFrame): All messages posted on the platform
        Network_db (dict): Historical network structure data
        ME_db (pd.DataFrame): Media effects tracking data
    """
    
    def __init__(self, n = 100, m = 400):
        """Initialize social media platform.
        
        Args:
            n (int, optional): Number of users. Defaults to 100.
            m (int, optional): Number of network edges. Defaults to 400.
        """
        self.p = .5  # Default activity probability
        self.n = n   # Number of users
        self.m = m   # Number of edges
        
        # Initialize user screen sizes (activity levels) - random integers 2-9
        self.l = np.random.randint(2, 10, n)
        
        # Create initial network structure
        self.G = random_graph_revised(self.n,self.m) 
        
        # Initialize user opinions uniformly between -1 and 1
        self.O = np.random.uniform(-1, 1, self.n)
        
        # Initialize data storage
        self.Opinions_db = {"Time_0": copy.deepcopy(self.O)}  # Opinion history
        self.Message_db = pd.DataFrame(columns = ["original_poster", "rt_poster","content", "rt_status"])
        self.Message_db["rt_status"] = self.Message_db["rt_status"].astype(bool)
        self.Network_db = {"Time_0": list(self.G.edges())}  # Network history
        self.ME_db = pd.DataFrame(columns = ["uid", "Time", "index", "effects"])  # Media effects
        self.ME_db["effects"] = self.ME_db["effects"].astype(bool)

        
    def screen_size(self, uid):
        """Calculate dynamic screen size for a user.
        
        Screen size determines how many messages a user sees at each time step.
        It's based on their base activity level plus random variation.
        
        Args:
            uid (int): User ID
            
        Returns:
            int: Number of messages the user will see (screen size)
        """
        l = self.l[uid] + np.random.randint(-2, 3)  # Base size + random variation
        return l
            
    def make_screen(self, uid, l, sub, include_media = True):
        """Create user's message screen based on their network and subscriptions.
        
        The screen contains the most recent messages from users they follow
        and optionally from media they subscribe to.
        
        Args:
            uid (int): User ID
            l (int): Screen size (number of messages to show)
            sub (list): List of media subscriptions
            include_media (bool, optional): Include media messages. Defaults to True.
            
        Returns:
            pd.DataFrame or None: DataFrame of messages if any exist, None otherwise
        """
        friends = list(self.G.successors(uid))
        if include_media:
            friends = friends + sub
        
        # Filter messages from followed users/media
        repost_by_friend = self.Message_db.rt_poster.isin(friends)
        screen = self.Message_db[repost_by_friend].tail(l)
        
        if len(screen) > 0:
            return screen
        else:
            return None
        
    def get_recent_o(self, uid):
        """Get user's current opinion.
        
        Args:
            uid (int): User ID
            
        Returns:
            float: User's current opinion value
        """
        return self.O[uid]

    def get_recent_neighors(self, uid):
        """Get users that this user follows.
        
        Args:
            uid (int): User ID
            
        Returns:
            networkx view: Iterator of users that uid follows
        """
        return self.G.successors(uid)
    
    def add_edge(self, uid, new_fri):
        """Add a new following relationship.
        
        Args:
            uid (int): User who will follow
            new_fri (int): User to be followed
        """
        self.G.add_edge(uid, new_fri)

    def remove_edge(self, uid, foe_target):
        """Remove a following relationship.
        
        Args:
            uid (int): User who will unfollow
            foe_target (int): User to be unfollowed
        """
        self.G.remove_edge(uid, foe_target)
        
    def add_message(self, message):
        """Add a new message to the platform.
        
        Args:
            message (pd.DataFrame): Message data with columns:
                                  ['original_poster', 'rt_poster', 'content', 'rt_status']
        """
        self.Message_db = pd.concat([self.Message_db, message], ignore_index = True, axis = 0)
    def update_Opinions_db(self, uid, new_o, t):
        """Update user's opinion and record in database.
        
        Args:
            uid (int): User ID
            new_o (float or None): New opinion value, or None if no change
            t (int): Current time step
        """
        if new_o:
            self.O[uid] = new_o
        self.Opinions_db["Time_"+str(t+1)] = copy.deepcopy(self.O)

    def update_Network_db(self, t):
        """Record current network structure.
        
        Args:
            t (int): Current time step
        """
        self.Network_db["Time_"+str(t+1)] = copy.deepcopy(list(self.G.edges())) 
    
    def update_ME_db(self, t, uid, fri, foe):
        """Record media effects for analysis.
        
        Tracks which messages had positive (fri) or negative (foe) effects
        on user behavior and opinion formation.
        
        Args:
            t (int): Current time step
            uid (int): User ID
            fri (pd.DataFrame or None): Messages that had positive influence
            foe (pd.DataFrame or None): Messages that had negative influence
        """
        if fri is not None:
            fri = fri.reset_index()
            fri["effects"] = True 
            fri["uid"] = uid
            fri["Time"] = t + 1
            fri_record = fri[["uid", "Time", "index", "effects"]]
            self.ME_db = pd.concat([self.ME_db, fri_record], axis= 0, ignore_index=True)
            
        if foe is not None:
            foe = foe.reset_index()
            foe["effects"] = False
            foe["uid"] = uid
            foe["Time"] = t + 1 
            foe_record = foe[["uid", "Time", "index", "effects"]]
            self.ME_db = pd.concat([self.ME_db, foe_record], ignore_index= True)
        
        
           
