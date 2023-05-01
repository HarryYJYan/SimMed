#!/bin/bash
#SBATCH -A general
#SBATCH -J SimMedi_test
#SBATCH -p gpu
#SBATCH -o SimMedi_test%j.txt
#SBATCH -e SimMedi_test%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=harryan@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=24G
#SBATCH --time=20:00:00
errcho(){ >&2 echo $@; }
source /N/u/harryan/BigRed200/mambaforge/etc/profile.d/conda.sh
conda activate SimMed
####################################################################
cd /N/u/harryan/BigRed200/SimMed/code
srun python analysis.py