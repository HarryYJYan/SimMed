# SimMed: Agent-Based Model for Mass Media Effects on Opinion Dynamics

## Overview

SimMed is an agent-based model designed to study how mass media systems influence opinion formation and polarization in social networks. The model implements cultivation theory principles to examine mainstreaming effects in high-choice media environments.

## Research Context

This codebase implements the simulation model described in the paper on mass media effects using agent-based modeling. The research addresses key questions about how media proliferation affects opinion dynamics, particularly examining:

- **Mainstreaming Effects**: How mass media creates convergence toward moderate opinions
- **Polarization vs. Homogenization**: Different patterns of opinion evolution
- **Media Proliferation**: Effects of having multiple competing media systems
- **Audience Reach**: How the scope of media influence affects outcomes

### Theoretical Framework

The model is grounded in **Cultivation Theory**, specifically examining:

- How repeated exposure to media content shapes perceptions
- Mainstreaming effects in fragmented media landscapes
- The interaction between social influence and media influence
- Opinion similarity thresholds and tolerance levels

## Model Architecture

### Core Components

1. **Social Media Platform** (`SocialMedia.py`)

   - Network of users connected by following relationships
   - Message posting and reposting system
   - Opinion tracking and evolution over time
   - Dynamic network structure with rewiring
2. **Mass Media Systems** (`Media.py`)

   - Multiple competing media outlets
   - Content generation based on audience opinions
   - Subscription-based audience model
   - Variable market shares and reach
3. **Individual Users** (`User.py`)

   - Opinion values on a continuous scale (-1 to 1)
   - Tolerance thresholds for opinion similarity
   - Social influence susceptibility
   - Content consumption and generation behaviors
4. **Activity Engine** (`activity.py`)

   - Coordinates user-media interactions
   - Handles opinion updates and social influence
   - Manages network rewiring dynamics
   - Controls cross-platform information flow

### Key Parameters

- **s (Audience Share)**: Proportion of users exposed to mass media (0-1)
- **N (Number of Media)**: Count of mass media systems in simulation
- **eta (Tolerance)**: Opinion similarity threshold for user interactions (0-1)
- **miu (Social Influence)**: Strength of peer influence on opinion updates (0-1)
- **n (Users)**: Number of agents in the social network (default: 100)
- **m (Edges)**: Number of connections in the initial network (default: 400)
- **T (Time Steps)**: Length of simulation (default: 10,000)

## Installation and Setup

### Prerequisites

```bash
# Python packages required
pip install numpy pandas networkx matplotlib seaborn scikit-learn scipy tqdm
```

### Repository Structure

```
SimMed/
├── code/                    # Main simulation code
│   ├── sim.py              # Main simulation orchestrator
│   ├── SocialMedia.py      # Social media platform implementation
│   ├── Media.py            # Mass media systems
│   ├── User.py             # Individual user agents
│   ├── activity.py         # Activity coordination functions
│   ├── analysis.py         # Analysis and batch processing
│   ├── baseline.py         # Baseline simulations (no media)
│   ├── vis.py              # Visualization functions
│   └── run.py              # Batch simulation runner
├── paper/                   # LaTeX paper (synced with Overleaf)
│   ├── main.tex            # Main paper document
│   ├── ref.bib             # Bibliography
│   ├── Figures/            # Paper figures
│   ├── Tables/             # Paper tables
│   └── .cursor/            # Cursor LaTeX configuration
├── individual/             # Individual-level analysis tools
├── analysis.ipynb          # Main analysis notebook
├── networks.ipynb          # Network analysis notebook
├── PARAMETERS.md           # Parameter documentation
├── ANALYSIS_GUIDE.md       # Analysis methodology
└── prototype/              # Early development prototypes
```

## Usage

### Basic Simulation

Run a single simulation with specific parameters:

```bash
cd code/
python sim.py 0.5 3 0.4
# Arguments: audience_share(s), num_media(N), tolerance(eta)
```

### Batch Simulations

For multiple runs with parameter sweeps:

```bash
python run.py 0.5 3 0.4 0 100
# Arguments: s, N, eta, start_iteration, end_iteration
```

### Python API Usage

```python
from code.sim import sim

# Run simulation with custom parameters
social_media, mass_media = sim(
    s=0.5,          # 50% audience reach
    N=3,            # 3 media systems
    eta=0.4,        # Tolerance threshold
    T=10000,        # 10,000 time steps
    n=100,          # 100 users
    miu=0.3,        # Social influence strength
    rand=0.2        # Noise level
)

# Access results
final_opinions = social_media.O
opinion_history = social_media.Opinions_db
message_data = social_media.Message_db
network_evolution = social_media.Network_db
```

### Baseline Simulation (No Media)

```python
# Simulate social dynamics without mass media influence
sm, md = sim(s=0, N=0, eta=1.0, include_media=False)
```

## Analysis and Visualization

### Opinion Distribution Analysis

The model tracks three main outcome patterns:

1. **Type A - Homogenization**: Single-peaked distribution around network mean
2. **Type B - Polarization**: Multi-peaked distribution with opinion clusters
3. **Type C - Mainstreaming**: Single-peaked distribution around moderate values

### Key Metrics

- **Opinion Entropy**: Measure of opinion diversity
- **Network Modularity**: Community structure detection
- **Media Effects**: Tracking influence of different content sources
- **Convergence Patterns**: Opinion evolution trajectories

### Visualization

```python
from code.vis import vis

# Generate standard visualization plots
fig = vis(social_media, s=0.5, N=3, eta=0.4)
```

## Parameter Sensitivity

### Critical Parameters

1. **Tolerance (eta)**: Lower values increase polarization risk
2. **Audience Share (s)**: Higher values strengthen media influence
3. **Number of Media (N)**: More systems can increase diversity
4. **Social Influence (miu)**: Affects convergence speed
5. **Noise (rand)**: Prevents complete consensus, maintains diversity

### Experimental Design

The model supports systematic parameter exploration:

```python
# Parameter sweep example
for s in [0.3, 0.5, 0.7]:
    for N in range(1, 6):
        for eta in [0.3, 0.4, 0.5]:
            sm, md = sim(s, N, eta)
            # Analyze results...
```

## Research Applications

### Hypothesis Testing

The model enables testing of key hypotheses:

1. **H1 (Mainstreaming)**: Mass media creates opinion convergence
2. **H2 (Proliferation-Diversification)**: More media systems increase opinion diversity
3. **Audience Reach Effects**: Media influence depends on exposure levels
4. **Tolerance Threshold Effects**: Opinion similarity requirements affect network dynamics

### Validation Studies

- Compare with empirical social media data
- Cross-validate with survey opinion data
- Test against known media effects from literature
- Robustness checks across parameter ranges

## Data Output

### Simulation Results

Each simulation generates:

- **opinions/**: Opinion evolution over time (Parquet format)
- **messages/**: All platform messages and metadata
- **networks/**: Network structure evolution (JSON format)
- **effects/**: Media influence tracking data
- **subscriptions/**: Media subscription dynamics

### Analysis Ready Format

Data is stored in analysis-friendly formats:

- Pandas DataFrames for opinion and message data
- NetworkX graphs for social structure
- JSON for metadata and configurations

## Paper Development Workflow

### LaTeX Paper Management

The `paper/` directory contains the research paper synchronized with Overleaf:

```bash
# Navigate to paper directory
cd paper/

# Pull latest changes from Overleaf (if collaborating)
git pull origin main

# Edit locally with Cursor LaTeX support
# - AI-assisted writing and formatting
# - Intelligent LaTeX autocomplete
# - Citation management

# Commit and push changes to Overleaf
git add .
git commit -m "Update methodology section"
git push origin main
```

### Cursor LaTeX Features

- **Scientific Writing Assistant**: AI help for clarity and coherence
- **LaTeX Syntax Support**: Intelligent autocomplete and error checking
- **Reference Management**: Citation formatting assistance
- **Table/Figure Editing**: Easy manipulation of complex LaTeX structures

## Computational Considerations

### Performance

- **Single Run**: ~10-30 seconds for standard parameters
- **Memory Usage**: ~50-200 MB depending on network size
- **Scaling**: Linear with time steps, quadratic with network size

### Parallel Processing

The codebase supports batch processing for parameter sweeps:

```bash
# Using GNU parallel or similar tools
parallel python run.py 0.5 {} 0.4 0 100 ::: 1 2 3 4 5
```

## Citation

If you use this code in your research, please cite:

```bibtex
@article{yan2024mainstreaming,
  title={Mainstreaming Revisited: Effects of Media Proliferation on Partisan Opinion Dynamics},
  author={Yan, Harry},
  journal={Under Review},
  year={2024}
}
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests for new features
4. Ensure code follows existing documentation standards
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions about the model or code:

- **Author**: Harry Yan
- **Email**: Harryyan@tamu.edu
- **Institution**: Texas A&M University

## Acknowledgments

This research builds on foundational work in:

- Cultivation Theory (Gerbner et al.)
- Agent-Based Modeling (Epstein & Axtell)
- Opinion Dynamics (DeGroot, Hegselmann-Krause)
- Network Science (Barabási, Watts & Strogatz)

Special thanks to reviewers and collaborators who provided feedback on the model design and implementation.
