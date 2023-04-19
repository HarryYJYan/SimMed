import matplotlib.pyplot as plt, seaborn as sns, pandas as pd
def vis(sm,p, s, N, T):
    fig, axes = plt.subplots(2, 2, figsize = (10, 10))
    axes = axes.flatten()
    pd.DataFrame(sm.Opinions_db).T.plot(figsize = (20,10), ax = axes[0])
    axes[0].legend().remove()
    axes[0].set_xlabel("Values")
    sns.heatmap(pd.DataFrame(sm.Opinions_db).sort_values(by = "Time_{}".format(str(T-1))), ax = axes[1])
#axes[1].set_title("Baseline", fontsize = 26)
    axes[1].set_ylabel("Agent Id")
    axes[1].set_xlabel("Time steps")
#axes[1].set_xticks(np.arange(10))
    axes[1].set_xticklabels([])
#axes[1].set_title("Baseline Consensus", fontsize = 26)
    sns.histplot(pd.DataFrame(sm.Opinions_db)["Time_0"], bins = 10, ax = axes[2], kde= True)
    sns.histplot(pd.DataFrame(sm.Opinions_db)["Time_{}".format(str(T-1))], bins = 10, ax = axes[3], kde = True, color = "orange")
#plt.suptitle("N = {}, p = {}, s = {}".format(str(N), str(p), str(s)), y = .95, fontsize = 20)
    plt.suptitle(f" active: {str(p)} share: {str(s)}  num_media: {str(N)} ", y = .95, fontsize = 20)
    plt.show()
    return fig


#ax.set_title("eta = {}, T/c = {}, condition = Polarized".format(str(eta), str(np.around(T/c,2))))
