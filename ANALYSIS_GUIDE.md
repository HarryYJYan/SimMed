# Analysis Guide for SimMed Results

## Overview

This guide provides comprehensive instructions for analyzing results from the SimMed agent-based model, including data interpretation, statistical analysis methods, and visualization techniques.

## Data Structure

### Output Files

Each simulation run generates several data files:

#### Opinion Data (`opinions/`)
- **Format**: Parquet files with columns for each time step
- **Structure**: Rows = users, Columns = time points
- **Content**: Opinion values [-1, 1] for all users over time

#### Message Data (`messages/`)
- **Format**: Parquet files with message metadata
- **Columns**:
  - `original_poster`: User/media who created content
  - `rt_poster`: User/media who posted/reposted
  - `content`: Opinion value of the message
  - `rt_status`: Boolean indicating if repost

#### Network Data (`networks/`)
- **Format**: JSON files with edge lists by time
- **Structure**: `{"Time_0": [(user1, user2), ...], "Time_1": [...]}`
- **Content**: Directed following relationships

#### Effects Data (`effects/`)
- **Format**: Parquet files tracking media influence
- **Columns**:
  - `uid`: User ID experiencing effect
  - `Time`: Time step of effect
  - `index`: Message index causing effect
  - `effects`: Boolean (True=positive, False=negative)

## Basic Analysis Workflow

### 1. Data Loading

```python
import pandas as pd
import numpy as np
import json

# Load opinion evolution
opinions = pd.read_parquet("opinions/0_opinions.parquet")

# Load messages
messages = pd.read_parquet("messages/0_messages.parquet")

# Load network evolution
with open("networks/0_networks.json", "r") as f:
    networks = json.load(f)

# Load effects data
effects = pd.read_parquet("effects/0_effects.parquet")
```

### 2. Opinion Analysis

#### Final Opinion Distribution
```python
final_opinions = opinions.iloc[:, -1]  # Last column
initial_opinions = opinions.iloc[:, 0]  # First column

# Calculate distribution statistics
mean_final = final_opinions.mean()
std_final = final_opinions.std()
```

#### Opinion Evolution Metrics
```python
from scipy.stats import entropy
from sklearn.mixture import GaussianMixture

# Calculate opinion entropy over time
entropies = []
for col in opinions.columns:
    hist, bins = np.histogram(opinions[col], bins=20, density=True)
    hist = hist[hist > 0]  # Remove zeros
    entropies.append(entropy(hist))

# Detect number of opinion clusters
final_opinions_reshaped = final_opinions.values.reshape(-1, 1)
gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(final_opinions_reshaped)
n_clusters = gmm.n_components
```

### 3. Pattern Classification

#### Outcome Types
Based on final opinion distributions:

```python
def classify_outcome(opinions_final, threshold_entropy=1.5, threshold_peaks=0.3):
    """
    Classify simulation outcome into three types:
    A: Homogenization (single peak around mean)
    B: Polarization (multiple peaks)
    C: Mainstreaming (single peak around moderate values)
    """
    hist, bins = np.histogram(opinions_final, bins=20)
    
    # Calculate entropy
    hist_norm = hist / hist.sum()
    hist_norm = hist_norm[hist_norm > 0]
    op_entropy = entropy(hist_norm)
    
    # Find peaks
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(hist, height=len(opinions_final)*threshold_peaks)
    
    # Classification logic
    if len(peaks) <= 1 and op_entropy < threshold_entropy:
        if abs(opinions_final.mean()) < 0.3:
            return "C"  # Mainstreaming
        else:
            return "A"  # Homogenization
    else:
        return "B"  # Polarization

outcome = classify_outcome(final_opinions)
```

### 4. Network Analysis

#### Network Evolution Metrics
```python
import networkx as nx

def analyze_network(edge_list):
    """Analyze network structure metrics"""
    G = nx.DiGraph(edge_list)
    
    metrics = {
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'density': nx.density(G),
        'clustering': nx.average_clustering(G),
        'components': nx.number_strongly_connected_components(G)
    }
    
    return metrics

# Analyze network evolution
network_metrics = {}
for time_key, edges in networks.items():
    network_metrics[time_key] = analyze_network(edges)
```

#### Community Detection
```python
import networkx.algorithms.community as nx_comm

# Final network analysis
final_edges = networks[list(networks.keys())[-1]]
G_final = nx.DiGraph(final_edges)

# Convert to undirected for community detection
G_undirected = G_final.to_undirected()

# Detect communities
communities = nx_comm.greedy_modularity_communities(G_undirected)
modularity = nx_comm.modularity(G_undirected, communities)
```

### 5. Media Effects Analysis

#### Media Influence Tracking
```python
# Analyze media effects over time
media_effects = effects.groupby('Time')['effects'].agg(['sum', 'count', 'mean'])

# Calculate cumulative media influence
cumulative_influence = media_effects['sum'].cumsum()

# Identify most influential media
message_influence = effects.merge(messages, left_on='index', right_index=True)
media_influence = message_influence.groupby('original_poster')['effects'].agg(['sum', 'count'])
```

### 6. Temporal Dynamics

#### Convergence Analysis
```python
def calculate_convergence_time(opinions, threshold=0.01):
    """Calculate time to convergence based on opinion variance"""
    variances = opinions.var(axis=0)
    
    # Find when variance stabilizes
    for i in range(len(variances)-100):
        if all(abs(variances[i+j] - variances[i+100]) < threshold for j in range(100)):
            return i
    
    return len(variances)  # No convergence

convergence_time = calculate_convergence_time(opinions)
```

#### Change Point Detection
```python
from scipy import stats

def detect_opinion_shifts(opinion_series, window=100):
    """Detect significant opinion change points"""
    change_points = []
    
    for i in range(window, len(opinion_series) - window):
        before = opinion_series[i-window:i]
        after = opinion_series[i:i+window]
        
        # T-test for significant difference
        t_stat, p_val = stats.ttest_ind(before, after)
        
        if p_val < 0.01:  # Significant change
            change_points.append(i)
    
    return change_points

# Detect change points for each user
user_changes = {}
for user_id in range(len(opinions)):
    user_opinion_series = opinions.iloc[user_id, :]
    changes = detect_opinion_shifts(user_opinion_series)
    user_changes[user_id] = changes
```

## Advanced Analysis Techniques

### 1. Parameter Sensitivity Analysis

```python
def sensitivity_analysis(results_dict, parameter_ranges):
    """
    Analyze how outcomes vary with parameter changes
    results_dict: {(s, N, eta): outcome_metrics}
    """
    sensitivity_results = {}
    
    for param in ['s', 'N', 'eta']:
        param_effects = []
        for params, outcome in results_dict.items():
            param_val = params[['s', 'N', 'eta'].index(param)]
            param_effects.append((param_val, outcome['entropy']))
        
        # Calculate correlation
        param_vals, outcomes = zip(*param_effects)
        correlation = np.corrcoef(param_vals, outcomes)[0,1]
        sensitivity_results[param] = correlation
    
    return sensitivity_results
```

### 2. Phase Diagram Construction

```python
def create_phase_diagram(results_grid, param1='s', param2='eta'):
    """Create phase diagram showing outcome types"""
    import matplotlib.pyplot as plt
    
    # Extract parameter values and outcomes
    param1_vals = []
    param2_vals = []
    outcomes = []
    
    for (s, N, eta), result in results_grid.items():
        param1_vals.append(locals()[param1])
        param2_vals.append(locals()[param2])
        outcomes.append(result['outcome_type'])
    
    # Create scatter plot with color coding
    outcome_colors = {'A': 'blue', 'B': 'red', 'C': 'green'}
    colors = [outcome_colors[o] for o in outcomes]
    
    plt.scatter(param1_vals, param2_vals, c=colors, alpha=0.7)
    plt.xlabel(param1)
    plt.ylabel(param2)
    plt.title('Phase Diagram of Simulation Outcomes')
    
    # Add legend
    for outcome, color in outcome_colors.items():
        plt.scatter([], [], c=color, label=f'Type {outcome}')
    plt.legend()
    
    return plt.gcf()
```

### 3. Statistical Testing

#### Hypothesis Testing Framework
```python
from scipy import stats

def test_mainstreaming_hypothesis(control_results, treatment_results):
    """
    Test if media presence creates mainstreaming effects
    control_results: outcomes without media (N=0)
    treatment_results: outcomes with media (N>0)
    """
    
    # Extract final opinion entropies
    control_entropies = [r['entropy'] for r in control_results]
    treatment_entropies = [r['entropy'] for r in treatment_results]
    
    # Test for significant difference
    t_stat, p_val = stats.ttest_ind(control_entropies, treatment_entropies)
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(control_entropies)-1)*np.var(control_entropies) + 
                         (len(treatment_entropies)-1)*np.var(treatment_entropies)) / 
                        (len(control_entropies) + len(treatment_entropies) - 2))
    
    cohens_d = (np.mean(control_entropies) - np.mean(treatment_entropies)) / pooled_std
    
    return {
        't_statistic': t_stat,
        'p_value': p_val,
        'effect_size': cohens_d,
        'significant': p_val < 0.05
    }
```

## Visualization Recipes

### 1. Opinion Evolution Plots

```python
def plot_opinion_evolution(opinions, sample_users=10):
    """Plot opinion trajectories for sample of users"""
    plt.figure(figsize=(12, 8))
    
    # Sample random users
    sampled_users = np.random.choice(len(opinions), sample_users, replace=False)
    
    for user in sampled_users:
        plt.plot(opinions.iloc[user, :], alpha=0.7, linewidth=1)
    
    plt.xlabel('Time Steps')
    plt.ylabel('Opinion Value')
    plt.title('Opinion Evolution Over Time')
    plt.grid(True, alpha=0.3)
    
    return plt.gcf()
```

### 2. Distribution Comparison

```python
def plot_distribution_comparison(initial_opinions, final_opinions):
    """Compare initial and final opinion distributions"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Initial distribution
    ax1.hist(initial_opinions, bins=20, alpha=0.7, density=True, color='blue')
    ax1.set_title('Initial Opinion Distribution')
    ax1.set_xlabel('Opinion Value')
    ax1.set_ylabel('Density')
    
    # Final distribution
    ax2.hist(final_opinions, bins=20, alpha=0.7, density=True, color='orange')
    ax2.set_title('Final Opinion Distribution')
    ax2.set_xlabel('Opinion Value')
    ax2.set_ylabel('Density')
    
    plt.tight_layout()
    return fig
```

### 3. Network Visualization

```python
def plot_network_evolution(networks, time_points=[0, -1]):
    """Visualize network at different time points"""
    fig, axes = plt.subplots(1, len(time_points), figsize=(6*len(time_points), 6))
    
    if len(time_points) == 1:
        axes = [axes]
    
    for i, t in enumerate(time_points):
        time_key = list(networks.keys())[t]
        edges = networks[time_key]
        
        G = nx.DiGraph(edges)
        pos = nx.spring_layout(G, seed=42)
        
        nx.draw(G, pos, ax=axes[i], node_size=30, node_color='lightblue',
                edge_color='gray', alpha=0.6, arrows=True, arrowsize=10)
        
        axes[i].set_title(f'Network at {time_key}')
    
    plt.tight_layout()
    return fig
```

## Quality Control

### Data Validation Checks

```python
def validate_simulation_data(opinions, messages, networks):
    """Perform quality control checks on simulation data"""
    checks = {}
    
    # Opinion bounds check
    checks['opinions_in_bounds'] = ((opinions >= -1) & (opinions <= 1)).all().all()
    
    # Message consistency check
    checks['message_posters_valid'] = messages['rt_poster'].notna().all()
    
    # Network consistency check
    time_keys = list(networks.keys())
    checks['network_temporal_consistency'] = len(time_keys) > 0
    
    # Data completeness check
    checks['no_missing_timepoints'] = len(opinions.columns) == len(time_keys)
    
    return checks
```

### Outlier Detection

```python
def detect_outliers(results_list, metric='entropy'):
    """Detect outlier simulations based on specified metric"""
    values = [r[metric] for r in results_list]
    
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1
    
    outlier_threshold_low = Q1 - 1.5 * IQR
    outlier_threshold_high = Q3 + 1.5 * IQR
    
    outliers = []
    for i, val in enumerate(values):
        if val < outlier_threshold_low or val > outlier_threshold_high:
            outliers.append(i)
    
    return outliers
```

## Reporting Templates

### Summary Statistics Table
```python
def generate_summary_table(results_dict):
    """Generate summary statistics table for publication"""
    import pandas as pd
    
    summary_data = []
    
    for params, result in results_dict.items():
        s, N, eta = params
        summary_data.append({
            'Audience_Share': s,
            'Media_Systems': N,
            'Tolerance': eta,
            'Final_Entropy': result['entropy'],
            'Outcome_Type': result['outcome_type'],
            'Convergence_Time': result['convergence_time'],
            'Final_Mean': result['final_mean'],
            'Final_Std': result['final_std']
        })
    
    return pd.DataFrame(summary_data)
```

This analysis guide provides a comprehensive framework for extracting insights from SimMed simulation results. Adapt these methods based on your specific research questions and hypotheses.
