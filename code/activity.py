import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
from User import User

def send_media_message(sm, md, Os, include_media = True):
    if include_media:
        for mid in md.mids:
            #print(med_ms)
            ms = md.media_message(mid, Os)
            if ms is not None:
                sm.add_message(ms) 

def sample_user(sm):
    uid = np.random.randint(sm.n)
    l = sm.screen_size(uid)
    #print(l)
    if l == 0:
        return None, 0
    else:
        return uid, l

def user_activity(uid, sm, md, eta, miu, l, subs, rand, include_media):
    o = sm.get_recent_o(uid)
    subs = md.find_subs(uid)
    user = User(uid, eta, miu, o, sm.G, subs, md.mids)
    screen = sm.make_screen(user.uid, l  , user.subs, include_media = include_media)
    fri = user.find_fri(screen)
    foe = user.find_foe(screen)
    new_o = user.update_opinion(fri, rand = rand)
    new_post = user.generate_post(fri)
    return user, fri, foe,  new_o, new_post


def update_network(user, prob_rewire, fri, foe, md, sm, mix = False):
    if np.random.random() < prob_rewire: 
        if foe is not None:
            foe_target = user.find_unfriend(foe)
            if str(foe_target)[0] == "m":
                md.cancel(user.uid, foe_target)
                #print(user.uid, "cancel" , foe_target)
                if not mix:
                    fri_target = user.find_friend(fri, sm.Message_db, output = "media")
                    md.subscribe(user.uid, fri_target)
            else:
                sm.remove_edge(user.uid, foe_target)
                #print(user.uid, "unfollow" , foe_target)
                if not mix:
                    fri_target = user.find_friend(fri, sm.Message_db, output = "agent")
                    sm.add_edge(user.uid, fri_target)
            if mix:
                fri_target = user.find_friend(fri, sm.Message_db, output = "mix", print_method = False)
                if str(fri_target)[0] == "m":
                    md.subscribe(user.uid, fri_target)
                else:
                    sm.add_edge(user.uid, fri_target)
