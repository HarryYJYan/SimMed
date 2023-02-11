import numpy as np, pandas as pd
from SocialMedia import SocialMedia
from User import User
from Media import MassMedia

def unfriend_friend(prob_rewire, user, fri, foe, sm, media_ids):
    q = np.random.random()
    if q< prob_rewire:
        unfriend = user.unfriend(foe)
        if unfriend == True:
            #print(str(user.uid), "unfriend a foe")
            new_friend = user.friend_repost(fri)
            if new_friend != True:
                #print(str(user.uid), "did not find a repost friend")
                recommend = sm.get_recomm_friends(user.uid, media_ids, user.eta)
                new_friend = user.friend_recommend(recommend)
                if new_friend != True:
                    #print(str(user.uid), "did not find a repost nor recommend friend")
                    new_friend = user.friend_random()
                    if new_friend != True:
                        print(str(user.uid), "Warning: NOT finding a random/repost/recommend friend")
                        
                #else:
                    #

#def mass_media_project(c, sm, t, para_list):
    
        #sm.add_message(mass_media.any_media(t, n2))                    

def sim(media_para, include_media = True, effect_record = True, T = 10000, eta =.5, miu =.3, prob_rewire = .3, rand =.25, n = 100, m = 400):  #rand,
    sm = SocialMedia(n= n, m = m)
    media_dict = {media_para[num]["id"]: MassMedia(c = media_para[num]["c"], 
                            p =  media_para[num]["p"], 
                            s =  media_para[num]["s"], 
                            id = media_para[num]["id"])
                            for num in media_para.keys()}
    media_ids = list(media_dict.keys())
    for k in media_ids:
        sm.Config_db[k] = media_dict[k].audience
    for t in np.arange(T):
        if include_media == True:
            for k in media_ids:
                #print(med_ms)
                ms = media_dict[k].media_message()
                if ms is not None:
                    sm.add_message(ms)       
        uid = np.random.randint(sm.n)
        l = sm.screen_size(uid)
        #print(l)
        if l == 0:
            pass
        else:
            o = sm.get_recent_o(uid)
            user = User(uid, eta, miu, o, sm.G, media_dict)
            screen = sm.make_screen(user.uid, l, user.sub, include_media = include_media)
            fri = user.find_fri(screen)
            foe = user.find_foe(screen)
            #print(fri)
            #print("XXXXXXX")
            ##
            new_o = user.update_opinion(fri, rand = rand)
            new_post = user.generate_post(fri)
            unfriend_friend(prob_rewire, user, fri, foe, sm, media_ids)
            sm.add_message(new_post)
            ##
            sm.update_Opinions_db(uid, new_o, t)
            sm.update_Network_db(t)
            if effect_record == True:
                sm.update_ME_db(t, uid, fri, foe)
    return sm#

if __name__ == "__main__":
    c = 1
    p = .5
    s = .9
    media_para = {1:{"c":c, "p": p, "s":s, "id":"Test_media" } }  #<-----------
    sm = sim(media_para = media_para, include_media = False, effect_record= True)
    from vis import vis
    vis(sm, c, p, s, media_para[1]["id"])

#ax.set_title("eta = {}, T/c = {}, condition = Polarized".format(str(eta), str(np.around(T/c,2))))
