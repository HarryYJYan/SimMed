#!/bin/bash
#SBATCH -A general
#SBATCH -p gpu
#SBATCH -J SM
#SBATCH -o SM%j.txt
#SBATCH -e SM%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=harryan@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8G
#SBATCH --time=4:00:00

errcho(){ >&2 echo $@; }
source /N/u/harryan/BigRed200/mambaforge/etc/profile.d/conda.sh
conda activate SimMed
####################################################################
cd /N/u/harryan/BigRed200/SimMed/code
s=$1
N=$2
e=$3
job_name="SM-${s}-${N}-${e}"

srun --exclusive --job-name="${job_name}" python run.py $s $N $e 100