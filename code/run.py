"""Batch Simulation Runner for Agent-Based Media Effects Model.

This module handles batch execution of simulations with systematic data storage.
It runs multiple iterations of the simulation with the same parameters and
saves all results in organized directory structures for later analysis.

Functions:
    run: Execute multiple simulation iterations and save results
    
Usage:
    python run.py <audience_share> <num_media> <tolerance> <start_iter> <end_iter>
    
Example:
    python run.py 0.5 3 0.4 0 100  # Run 100 iterations with specified parameters
"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import pandas as pd, json as js
from sim import sim
import argparse

ROOT_DIR = "/N/slate/harryan/sim_data"

def run(s, N, eta, start, end):
    """Execute batch simulations and save results.
    
    Runs multiple iterations of the simulation with identical parameters
    and saves all generated data (opinions, messages, networks, effects)
    in organized directory structures.
    
    Args:
        s (float): Audience share parameter (0-1)
        N (int): Number of mass media systems
        eta (float): Tolerance threshold for opinion similarity (0-1)
        start (int): Starting iteration number
        end (int): Ending iteration number (exclusive)
        
    Directory Structure:
        ROOT_DIR/N{N}/s{s}eta{eta}/
        ├── messages/     # Message data for each iteration
        ├── opinions/     # Opinion evolution data
        ├── networks/     # Network structure evolution
        ├── effects/      # Media effects tracking
        ├── screensizes/  # User activity levels
        └── subscriptions/ # Media subscription data
    
    Example:
        >>> run(s=0.5, N=3, eta=0.4, start=0, end=10)
        # Runs 10 iterations and saves all results
    """
    # Create directory structure
    cwd = ROOT_DIR + f"/N{str(N)}/s{str(s)[-1]}eta{str(eta)[-1]}/" 
    if not os.path.exists(cwd):
        os.makedirs(cwd, exist_ok=True)
        for folder in ["messages", "opinions", "networks", "effects", "screensizes", "subscriptions"]:
            os.makedirs(cwd + folder)
    
    # Run simulations for specified iteration range
    for iteration in range(start, end):
        # Run simulation (with or without media)
        if N != 0:
            sm, md = sim(s, N, eta)
        else:
            sm, md = sim(0, 1, eta, include_media=False)
        
        # Save opinion evolution data
        opinions = pd.DataFrame(sm.Opinions_db)
        opinions.to_parquet(f"{cwd}/opinions/{str(iteration)}_opinions.parquet")
        
        # Save message data
        messages = sm.Message_db
        messages.original_poster = messages.original_poster.astype(str)
        messages.rt_poster = messages.rt_poster.astype(str)
        messages.to_parquet(f"{cwd}/messages/{str(iteration)}_messages.parquet")
        
        # Save network evolution data
        with open(f"{cwd}/networks/{str(iteration)}_networks.json", "w") as f:
            js.dump(sm.Network_db, f) 
        
        # Save media effects data
        effects = sm.ME_db 
        effects.to_parquet(f"{cwd}/effects/{str(iteration)}_effects.parquet")
        
        # Save additional data for media simulations
        if N != 0:
            # Save user screen sizes
            with open(f"{cwd}/screensizes/{str(iteration)}_screensizes.json", "w") as f:
                js.dump([int(x) for x in sm.l], f)
            
            # Save subscription data
            with open(f"{cwd}/subscriptions/{str(iteration)}_subscriptions.json", "w") as f:
                js.dump(md.Subs_db, f)

if __name__ == '__main__':
    # Command-line interface for batch simulation execution
    parser = argparse.ArgumentParser(
        description='Run batch simulations of agent-based media effects model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py 0.5 3 0.4 0 100    # 100 iterations with s=0.5, N=3, eta=0.4
    python run.py 0.7 1 0.3 0 50     # 50 iterations with different parameters
    python run.py 0 0 1.0 0 10       # Baseline simulation (no media)
        """
    )

    # Required positional arguments
    parser.add_argument('s', type=float, 
                       help='Audience share/reach parameter (0-1)')
    parser.add_argument('N', type=int, 
                       help='Number of mass media systems')
    parser.add_argument('eta', type=float, 
                       help='Tolerance level for opinion similarity (0-1)')
    parser.add_argument('start', type=int, 
                       help='Starting iteration number')
    parser.add_argument('end', type=int, 
                       help='Ending iteration number (exclusive)')

    # Parse arguments and run
    args = parser.parse_args()
    
    print(f"Starting batch simulation:")
    print(f"  Audience share (s): {args.s}")
    print(f"  Number of media (N): {args.N}")
    print(f"  Tolerance (eta): {args.eta}")
    print(f"  Iterations: {args.start} to {args.end-1} ({args.end-args.start} total)")
    
    run(args.s, args.N, args.eta, args.start, args.end)
    print("Batch simulation completed.")
