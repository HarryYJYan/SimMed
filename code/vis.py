"""Visualization Module for Agent-Based Media Effects Simulation.

This module provides visualization functions for analyzing simulation results,
including opinion evolution plots, heatmaps, and distribution analysis.

Functions:
    vis: Create comprehensive visualization dashboard for simulation results
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import matplotlib.pyplot as plt, seaborn as sns, pandas as pd

def vis(sm, s, N, eta):
    """Create comprehensive visualization dashboard for simulation results.
    
    Generates a 2x2 subplot layout showing:
    1. Opinion evolution over time (line plot)
    2. Opinion heatmap sorted by final values
    3. Initial opinion distribution histogram
    4. Final opinion distribution histogram
    
    Args:
        sm (SocialMedia): Social media simulation results
        s (float): Audience share parameter
        N (int): Number of media systems
        eta (float): Tolerance threshold
        
    Returns:
        matplotlib.figure.Figure: The generated figure object
        
    Example:
        >>> from sim import sim
        >>> sm, md = sim(s=0.5, N=3, eta=0.4)
        >>> fig = vis(sm, 0.5, 3, 0.4)
        >>> plt.show()
    """
    # Create 2x2 subplot layout
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    
    # Convert opinion database to DataFrame
    data = pd.DataFrame(sm.Opinions_db)
    
    # Plot 1: Opinion evolution over time
    data.T.plot(figsize=(20, 10), ax=axes[0])
    axes[0].legend().remove()
    axes[0].set_xlabel("Time Steps")
    axes[0].set_ylabel("Opinion Values")
    axes[0].set_title("Opinion Evolution Over Time")
    
    # Plot 2: Opinion heatmap sorted by final values
    sns.heatmap(data.sort_values(by=data.columns[-1]), ax=axes[1])
    axes[1].set_ylabel("Agent ID (sorted by final opinion)")
    axes[1].set_xlabel("Time Steps")
    axes[1].set_xticklabels([])
    axes[1].set_title("Opinion Trajectory Heatmap")
    
    # Plot 3: Initial opinion distribution
    sns.histplot(data["Time_0"], bins=10, ax=axes[2], kde=True)
    axes[2].set_xlabel("Opinion Value")
    axes[2].set_ylabel("Frequency")
    axes[2].set_title("Initial Opinion Distribution")
    
    # Plot 4: Final opinion distribution
    sns.histplot(data[data.columns[-1]], bins=10, ax=axes[3], kde=True, color="orange")
    axes[3].set_xlabel("Opinion Value")
    axes[3].set_ylabel("Frequency")
    axes[3].set_title("Final Opinion Distribution")
    
    # Add overall title with parameters
    plt.suptitle(
        f"Simulation Results - Share: {s}, Media Systems: {N}, Tolerance: {eta}", 
        y=0.95, fontsize=16
    )
    
    plt.tight_layout()
    plt.show()
    return fig

if __name__ == '__main__':
    from sim import sim
    s, N, eta = .5, 2, .4
    sm, md = sim(s, N, eta)
    fig = vis(sm, s, N, eta)
    plt.show()

#ax.set_title("eta = {}, T/c = {}, condition = Polarized".format(str(eta), str(np.around(T/c,2))))
