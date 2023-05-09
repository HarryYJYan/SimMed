import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np

def entropy_continuous(x, nbins=100):
    # Define bins
    bins = np.linspace(-1, 1, nbins+1)
    
    # Bin the data
    counts, _ = np.histogram(x, bins)
    
    # Compute proportions
    props = counts / np.sum(counts)
    
    # Compute entropies
    eps = np.finfo(float).eps # small number to avoid log(0)
    entropies = -props * np.log2(props+eps)
    
    # Compute total entropy
    entropy = np.sum(entropies)
    
    return entropy