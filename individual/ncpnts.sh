#!/bin/bash
#SBATCH -A general
#SBATCH -p gpu
#SBATCH -J cpnts
#SBATCH -o cpnts%j.txt
#SBATCH -e cpnts%j.err
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
cd /N/u/harryan/BigRed200/SimMed/individual
srun python run_ncpnts.py $s $e 