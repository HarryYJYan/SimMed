# Model Parameters Guide

## Overview

This document provides detailed information about all parameters in the SimMed agent-based model, including their theoretical justification, valid ranges, and effects on simulation outcomes.

## Core Simulation Parameters

### Required Parameters

#### `s` - Audience Share/Reach
- **Type**: float (0.0 - 1.0)
- **Description**: Proportion of users who are exposed to mass media content
- **Theoretical Basis**: Represents media penetration and reach in the population
- **Effects**: 
  - Higher values increase media influence on opinion dynamics
  - s=0 creates baseline condition with no media exposure
  - s=1 means all users are potentially exposed to media content
- **Typical Values**: 0.3, 0.5, 0.7

#### `N` - Number of Media Systems
- **Type**: int (0 - 10)
- **Description**: Number of competing mass media systems in the simulation
- **Theoretical Basis**: Models media landscape diversity and competition
- **Effects**:
  - N=0 creates social-only baseline
  - N=1 tests single dominant media influence
  - N>1 examines media proliferation effects
- **Typical Values**: 0, 1, 3, 5

#### `eta` - Tolerance Threshold
- **Type**: float (0.0 - 1.0)
- **Description**: Opinion similarity threshold for user interactions
- **Theoretical Basis**: Based on bounded confidence models (Hegselmann-Krause)
- **Effects**:
  - Lower values increase polarization potential
  - Higher values promote consensus formation
  - eta=0.5 is critical threshold in many studies
- **Typical Values**: 0.3, 0.4, 0.5

### Optional Parameters

#### `p` - Media Activity Probability
- **Type**: float (0.0 - 1.0)
- **Default**: 0.5
- **Description**: Probability that each media system posts content at each time step
- **Effects**: Controls frequency of media message generation

#### `miu` - Social Influence Strength  
- **Type**: float (0.0 - 1.0)
- **Default**: 0.3
- **Description**: Magnitude of opinion change from social exposure
- **Theoretical Basis**: Social influence parameter in opinion dynamics models
- **Effects**: Higher values create faster opinion convergence

#### `rand` - Noise Level
- **Type**: float (0.0 - 0.5)
- **Default**: 0.2
- **Description**: Random noise added to opinion updates
- **Purpose**: Prevents complete consensus and maintains opinion diversity
- **Effects**: Higher values maintain more opinion variance

#### `prob_rewire` - Rewiring Probability
- **Type**: float (0.0 - 1.0)
- **Default**: 0.3
- **Description**: Probability of network rewiring (follow/unfollow) at each time step
- **Effects**: Controls network adaptation speed

### Network Parameters

#### `n` - Number of Users
- **Type**: int (50 - 1000)
- **Default**: 100
- **Description**: Total number of user agents in the simulation
- **Computational**: Linear effect on runtime

#### `m` - Number of Edges
- **Type**: int (n - 5*n)
- **Default**: 400 (for n=100)
- **Description**: Total directed edges in initial network
- **Network Density**: m/(n*(n-1)) typical range 0.02-0.1

#### `T` - Time Steps
- **Type**: int (1000 - 50000)
- **Default**: 10000
- **Description**: Length of simulation in discrete time steps
- **Convergence**: Most systems stabilize within 5000-10000 steps

### Advanced Parameters

#### `mix` - Cross-cutting Exposure
- **Type**: bool
- **Default**: False
- **Description**: Allow users to replace social connections with media subscriptions
- **Theory**: Tests homophily vs. heterophily in network formation

#### `include_media` - Media Inclusion
- **Type**: bool
- **Default**: True
- **Description**: Include mass media systems in simulation
- **Usage**: Set False for baseline social-only simulations

#### `effect_record` - Effect Tracking
- **Type**: bool
- **Default**: True
- **Description**: Record detailed media effects data
- **Performance**: Slight computational overhead when enabled

## Parameter Interactions

### Critical Combinations

1. **Polarization Risk**: Low eta + High miu + Low rand
2. **Mainstreaming Conditions**: Moderate eta + Media presence + Sufficient reach
3. **Homogenization**: High eta + High miu + Long time
4. **Fragmentation**: Low reach + Multiple media + Low tolerance

### Robustness Testing

Recommended parameter sweeps for robustness analysis:

```python
# Tolerance sensitivity
eta_values = [0.2, 0.3, 0.4, 0.5, 0.6]

# Media influence scaling
s_values = [0.1, 0.3, 0.5, 0.7, 0.9]

# Media diversity effects
N_values = [0, 1, 2, 3, 4, 5]

# Social influence scaling
miu_values = [0.1, 0.2, 0.3, 0.4, 0.5]
```

## Parameter Validation

### Theoretical Constraints

- **Opinion Range**: All opinions bounded in [-1, 1]
- **Probability Constraints**: All probability parameters in [0, 1]
- **Network Validity**: m should not exceed n*(n-1)
- **Convergence**: T should be sufficient for system stabilization

### Empirical Calibration

Parameters can be calibrated against:
- Survey data on opinion distributions
- Social media network statistics
- Media consumption patterns
- Opinion change rates from longitudinal studies

## Sensitivity Analysis Results

Based on extensive simulation testing:

### High Sensitivity Parameters
1. **eta (Tolerance)**: Small changes dramatically affect outcomes
2. **s (Audience Share)**: Linear relationship with media influence
3. **N (Media Number)**: Non-linear effects on diversity

### Low Sensitivity Parameters
1. **rand (Noise)**: Robust across reasonable ranges
2. **prob_rewire**: Limited effect on final outcomes
3. **p (Media Activity)**: Mainly affects convergence speed

## Parameter Selection Guidelines

### For Hypothesis Testing
- **Mainstreaming**: eta=0.4-0.5, s=0.5-0.7, N=1-3
- **Polarization**: eta=0.2-0.3, varied social influence
- **Media Competition**: Fixed eta and s, vary N

### For Empirical Validation
- Match eta to empirical tolerance data
- Calibrate s to actual media reach statistics
- Set N based on real media landscape

### For Robustness Checks
- Test all parameters ±20% from baseline
- Examine boundary conditions (0, 1 values)
- Verify monotonic relationships where expected

## Common Parameter Issues

### Numerical Stability
- Very low eta (<0.1) can cause network fragmentation
- Very high rand (>0.3) can prevent convergence
- Extreme miu values (>0.8) can cause oscillations

### Interpretation Warnings
- Parameter effects are often non-linear
- Interaction effects can dominate main effects
- Context dependency varies across parameter ranges

## References

- DeGroot, M. H. (1974). Reaching a consensus. Journal of the American Statistical Association
- Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence
- Deffuant, G., et al. (2000). Mixing beliefs among interacting agents
