#!/bin/bash
#SBATCH -A general
#SBATCH -J SimMed
#SBATCH -p gpu
#SBATCH --mail-user=username@iu.edu
#SBATCH --mail-type=FAIL
#SBATCH -o SimMedi%j.txt
#SBATCH -e SimMedi%j.err
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=1G

source /N/u/harryan/BigRed200/mambaforge/etc/profile.d/conda.sh
conda activate SimMed
####################################################################
cd /N/u/harryan/BigRed200/SimMed/code

s_values=(.1 .3 .5 .7 .9)
N_values=(1 2 3 4 5)

# Loop over all combinations of s, N, and eta
for s in "${s_values[@]}"
do
  for N in "${N_values[@]}"
  do
    # Construct the command to run the program
    command="python run.py $s $N .2 100"
    # Submit the command as a job using Slurm
    srun --exclusive --job-name="SimMed_${s}_${N}_2" $command &
  done
done

wait
