# Notebooks Documentation

## Overview

This directory contains Jupyter notebooks for analyzing simulation results and exploring the agent-based model behavior.

## Available Notebooks

### `analysis.ipynb`
- **Purpose**: Main analysis workflow for processing simulation results
- **Content**: 
  - Data loading and preprocessing
  - Opinion distribution analysis
  - Pattern classification (homogenization, polarization, mainstreaming)
  - Statistical testing and visualization
- **Usage**: Start here for analyzing completed simulation runs

### `networks.ipynb`
- **Purpose**: Network structure analysis and community detection
- **Content**:
  - Social network evolution analysis
  - Community structure detection
  - Network modularity calculations
  - Graph visualization techniques
- **Usage**: For understanding social structure dynamics

### `prototype/prototype.ipynb`
- **Purpose**: Early development and testing notebook
- **Content**: Initial model development and parameter testing
- **Status**: Historical reference, may contain outdated code

## Getting Started

1. **Setup Environment**:
   ```bash
   pip install jupyter pandas numpy matplotlib seaborn networkx scikit-learn
   ```

2. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

3. **Run Analysis**:
   - Start with `analysis.ipynb` for basic analysis
   - Use `networks.ipynb` for network-specific questions
   - Modify notebooks for your specific research questions

## Data Requirements

The notebooks expect simulation data in the following structure:
```
data/
├── opinions/          # Opinion evolution data
├── messages/          # Message and interaction data
├── networks/          # Network structure evolution
└── effects/           # Media effects tracking
```

## Common Workflows

### Basic Analysis Pipeline
1. Load simulation results
2. Calculate outcome metrics (entropy, clustering, etc.)
3. Classify outcome type (A, B, or C)
4. Generate visualizations
5. Perform statistical tests

### Network Analysis Pipeline
1. Load network evolution data
2. Calculate network metrics over time
3. Detect community structure
4. Analyze network-opinion relationships
5. Visualize network dynamics

## Customization

### Adding New Analysis
- Create new cells in existing notebooks
- Follow established data loading patterns
- Use consistent variable naming
- Document new metrics and visualizations

### Parameter Studies
- Modify data loading paths for different parameter sets
- Create loops for batch analysis
- Save results in standardized formats
- Generate comparison plots across conditions

## Best Practices

1. **Data Management**: Keep raw data separate from processed results
2. **Version Control**: Save notebook outputs before major changes
3. **Documentation**: Add markdown cells explaining analysis steps
4. **Reproducibility**: Set random seeds where applicable
5. **Performance**: Use vectorized operations for large datasets

## Troubleshooting

### Common Issues
- **Memory Problems**: Use data chunking for large simulation sets
- **Missing Dependencies**: Install packages as needed
- **Data Loading Errors**: Check file paths and data structure
- **Visualization Issues**: Adjust plot parameters for your data size

### Performance Tips
- Load only necessary data columns
- Use sampling for exploratory analysis
- Cache intermediate results
- Consider using Dask for very large datasets
