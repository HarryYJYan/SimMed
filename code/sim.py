import numpy as np, pandas as pd
from SocialMedia import SocialMedia
from User import User
from Media import MassMedia
from tqdm import tqdm

def send_media_messege(sm, md, Os, include_media = True):
    if include_media:
        for mid in md.mids:
            #print(med_ms)
            ms = md.media_messege(mid, Os)
            if ms is not None:
                sm.add_messege(ms) 

def sample_user(sm):
    uid = np.random.randint(sm.n)
    l = sm.screen_size(uid)
    #print(l)
    if l == 0:
        return None, 0
    else:
        return uid, l

def user_activity(uid, sm, md, eta, miu, l, subs, mids,  rand, include_media):
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
                    fri_target = user.find_friend(fri, sm.Messege_db, output = "media")
                    md.subscribe(user.uid, fri_target)
            else:
                sm.remove_edge(user.uid, foe_target)
                #print(user.uid, "unfollow" , foe_target)
                if not mix:
                    fri_target = user.find_friend(fri, sm.Messege_db, output = "agent")
                    sm.add_edge(user.uid, fri_target)
            if mix:
                fri_target = user.find_friend(fri, sm.Messege_db, output = "mix", print_method = False)
                if str(fri_target)[0] == "m":
                    md.subscribe(user.uid, fri_target)
                else:
                    sm.add_edge(user.uid, fri_target)


          
def sim(p, s, N, mix = False, include_media = True, effect_record = True, n = 100, m = 400, T = 10000, eta = .5, miu = .3, prob_rewire = .3, rand =.2):  #rand,
    sm = SocialMedia(n= n, m = m) 
    md = MassMedia(p, s, N)
    for t in tqdm(np.arange(T), desc = "Run: "):
        Os = sm.Opinions_db[list(sm.Opinions_db.keys())[-1]]
        send_media_messege(sm, md, Os, include_media)
        uid, l = sample_user(sm)
        if uid:
            subs = md.find_subs(uid)
            user, fri, foe, new_o, new_post = user_activity(uid, sm, md, eta, miu, l, subs, md.mids, rand, include_media)
            sm.add_messege(new_post)
            sm.update_Opinions_db(uid, new_o, t)
            if effect_record == True:
                sm.update_ME_db(t, uid, fri, foe)
            update_network(user, prob_rewire, fri, foe, md, sm, mix = mix)
            sm.update_Network_db(t)
            md.update_Sub_DB(t)  
    return sm, md#

if __name__ == "__main__":
    N = 1
    p = .5
    s = .9
    T = 10000
    sm, md = sim(p, s, N, include_media = False, effect_record= True, T = T)
    from vis import vis
    vis(sm, p, s, N, T)

#ax.set_title("eta = {}, T/c = {}, condition = Polarized".format(str(eta), str(np.around(T/c,2))))
