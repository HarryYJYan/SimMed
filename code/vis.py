import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import matplotlib.pyplot as plt, seaborn as sns, pandas as pd

def vis(sm, s, N ,eta):
    fig, axes = plt.subplots(2, 2, figsize = (10, 10))
    axes = axes.flatten()
    data = pd.DataFrame(sm.Opinions_db)
    data.T.plot(figsize = (20,10), ax = axes[0])
    axes[0].legend().remove()
    axes[0].set_xlabel("Values")
    sns.heatmap(data.sort_values(by = data.columns[-1]), ax = axes[1])
#axes[1].set_title("Baseline", fontsize = 26)
    axes[1].set_ylabel("Agent Id")
    axes[1].set_xlabel("Time steps")
#axes[1].set_xticks(np.arange(10))
    axes[1].set_xticklabels([])
#axes[1].set_title("Baseline Consensus", fontsize = 26)
    sns.histplot(data["Time_0"], bins = 10, ax = axes[2], kde= True)
    sns.histplot(data[data.columns[-1]], bins = 10, ax = axes[3], kde = True, color = "orange")
#plt.suptitle("N = {}, p = {}, s = {}".format(str(N), str(p), str(s)), y = .95, fontsize = 20)
    plt.suptitle(f"Share: {str(s)}  Num_media: {str(N)}: Tolerance: {str(eta)} ", y = .95, fontsize = 20)
    plt.show()
    return fig

if __name__ == '__main__':
    from sim import sim
    s, N, eta = .5, 2, .4
    sm, md = sim(s, N, eta)
    fig = vis(sm, s, N, eta)
    plt.show()

#ax.set_title("eta = {}, T/c = {}, condition = Polarized".format(str(eta), str(np.around(T/c,2))))
