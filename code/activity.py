"""Activity Module for Agent-Based Media Effects Simulation.

This module contains the core activity functions that drive the simulation.
It coordinates interactions between social media users, mass media systems,
and network dynamics during each time step of the simulation.

Functions handle:
- Media message generation and posting
- User sampling and activity simulation
- Opinion updates and social influence
- Network rewiring based on opinion similarity
- Cross-platform interactions between social and mass media

Functions:
    send_media_message: Generate and post media content
    sample_user: Select a user for activity
    user_activity: Simulate complete user interaction cycle
    update_network: Handle following/unfollowing behavior
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
from User import User

def send_media_message(sm, md, Os, include_media=True):
    """Generate and post messages from mass media systems.
    
    Each media system has a chance to post content based on the current
    opinion distribution of their subscribers.
    
    Args:
        sm (SocialMedia): Social media platform instance
        md (MassMedia): Mass media systems instance
        Os (np.ndarray): Current opinion state of all users
        include_media (bool, optional): Whether to include media. Defaults to True.
    """
    if include_media:
        for mid in md.mids:
            # Each media system attempts to generate a message
            ms = md.media_message(mid, Os)
            if ms is not None:
                sm.add_message(ms) 

def sample_user(sm):
    """Randomly select a user for activity and determine their screen size.
    
    Args:
        sm (SocialMedia): Social media platform instance
        
    Returns:
        tuple: (user_id, screen_size) or (None, 0) if user inactive
    """
    uid = np.random.randint(sm.n)
    l = sm.screen_size(uid)
    
    if l == 0:
        return None, 0  # User is inactive this time step
    else:
        return uid, l

def user_activity(uid, sm, md, eta, miu, l, subs, rand, include_media):
    """Simulate complete user activity cycle for one time step.
    
    This function handles the full sequence of user behavior:
    1. Create user instance with current state
    2. Generate personalized content screen
    3. Identify friendly and hostile content
    4. Update opinion based on social influence
    5. Generate new post or repost
    
    Args:
        uid (int): User ID
        sm (SocialMedia): Social media platform instance
        md (MassMedia): Mass media systems instance
        eta (float): Tolerance threshold for opinion similarity
        miu (float): Strength of social influence
        l (int): Screen size (number of messages to show)
        subs (list): User's media subscriptions
        rand (float): Noise level in opinion updates
        include_media (bool): Whether to include media content
        
    Returns:
        tuple: (user_instance, friendly_messages, hostile_messages, new_opinion, new_post)
    """
    # Get user's current opinion and subscriptions
    o = sm.get_recent_o(uid)
    subs = md.find_subs(uid)
    
    # Create user instance
    user = User(uid, eta, miu, o, sm.G, subs, md.mids)
    
    # Generate personalized content screen
    screen = sm.make_screen(user.uid, l, user.subs, include_media=include_media)
    
    # Categorize content as friendly or hostile
    fri = user.find_fri(screen)
    foe = user.find_foe(screen)
    
    # Update opinion based on social influence
    new_o = user.update_opinion(fri, rand=rand)
    
    # Generate new content
    new_post = user.generate_post(fri)
    
    return user, fri, foe, new_o, new_post


def update_network(user, prob_rewire, fri, foe, md, sm, mix=False):
    """Handle network rewiring based on user interactions and opinions.
    
    Users may unfollow sources of hostile content and follow sources of
    friendly content, based on a rewiring probability. The rewiring can
    be homophilic (like-with-like) or mixed (cross-cutting exposure).
    
    Args:
        user (User): User instance
        prob_rewire (float): Probability of network rewiring (0-1)
        fri (pd.DataFrame or None): Friendly messages
        foe (pd.DataFrame or None): Hostile messages
        md (MassMedia): Mass media systems instance
        sm (SocialMedia): Social media platform instance
        mix (bool, optional): Allow cross-cutting exposure. Defaults to False.
    """
    if np.random.random() < prob_rewire: 
        if foe is not None:
            # Select a target to unfollow from hostile sources
            foe_target = user.find_unfriend(foe)
            
            if str(foe_target)[0] == "m":
                # Unfollowing a media system
                md.cancel(user.uid, foe_target)
                
                if not mix:
                    # Homophilic rewiring: replace with similar media
                    fri_target = user.find_friend(fri, sm.Message_db, output="media")
                    md.subscribe(user.uid, fri_target)
            else:
                # Unfollowing a user
                sm.remove_edge(user.uid, foe_target)
                
                if not mix:
                    # Homophilic rewiring: replace with similar user
                    fri_target = user.find_friend(fri, sm.Message_db, output="agent")
                    sm.add_edge(user.uid, fri_target)
                    
            if mix:
                # Cross-cutting rewiring: can replace with any type
                fri_target = user.find_friend(fri, sm.Message_db, output="mix", print_method=False)
                if str(fri_target)[0] == "m":
                    md.subscribe(user.uid, fri_target)
                else:
                    sm.add_edge(user.uid, fri_target)
