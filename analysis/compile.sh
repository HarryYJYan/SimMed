#!/bin/bash
#SBATCH -A general
#SBATCH -p gpu
#SBATCH -J Compile
#SBATCH -o Compile%j.txt
#SBATCH -e Compile%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=harryan@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8G
#SBATCH --time=2:00:00

errcho(){ >&2 echo $@; }
source /N/u/harryan/Carbonate/mambaforge/etc/profile.d/conda.sh
conda activate SimMedEffects
####################################################################
s=$1
e=$2
pos=$3
cd /N/u/harryan/Carbonate/SimMed/analysis
srun --exclusive python run_compile.py $s $e $pos