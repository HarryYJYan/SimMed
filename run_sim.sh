#!/bin/bash
#SBATCH -A general
#SBATCH -J SimMedi
#SBATCH -p gpu
#SBATCH -o SimMedi%j.txt
#SBATCH -e SimMedi%j.err
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=1G
errcho(){ >&2 echo $@; }
source /N/u/harryan/BigRed200/mambaforge/etc/profile.d/conda.sh
conda activate SimMed
####################################################################
cd /N/u/harryan/BigRed200/SimMed/code

s_values=(.1 .3 .5 .7 .9)
N_values=(1 2 3 4 5)
eta_values=(0.2 0.5 0.8)

# Loop over all combinations of s, N, and eta
for s in "${s_values[@]}"
do
  for N in "${N_values[@]}"
  do
    for eta in "${eta_values[@]}"
    do
      for iteration in {0..99}
      do
        # Construct the command to run the program
        command="python run.py $s $N $eta $iteration"
        # Submit the command as a job using Slurm
        sbatch $0 <<< $command
      done
    done
  done
done

