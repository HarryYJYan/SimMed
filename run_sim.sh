#!/bin/bash
#SBATCH -A general
#SBATCH -J SimMed
#SBATCH -p gpu
#SBATCH --mail-user=username@iu.edu
#SBATCH --mail-type=FAIL
#SBATCH -o SimMed%j.txt
#SBATCH -e SimMed%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=1G

source /N/u/harryan/BigRed200/mambaforge/etc/profile.d/conda.sh
conda activate SimMed
####################################################################
cd /N/u/harryan/Carbonate/SimMed/code

s_values=(.1 .3 .5 .7 .9)
N_values=(1 2 3 4 5)

# Loop over all combinations of s, N, and eta
for s in "${s_values[@]}"
do
  for N in "${N_values[@]}"
  do
    # Construct the command to run the program
    #command="python run.py $s $N .8 100"
    # Submit the command as a job using Slurm
    srun --exclusive --job-name="SimMed_${s}_${N}_8" python run.py $s $N .8 100 &
  done
done

wait
