import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

# Define the ranges of s, N, eta, and iteration to iterate over
s_values = [0.1, 0.3, 0.5, 0.7, 0.9]
N_values = [1, 2, 3, 4, 5]
eta_values = [0.2, 0.5, 0.8]
iteration_values = range(100)

# Define the input and output files for each job
def input_file(s, N, eta, iteration):
    return f"input/{s}_{N}_{eta}_{iteration}.txt"

def output_file(s, N, eta, iteration):
    return f"output/{s}_{N}_{eta}_{iteration}.txt"

# Define the rule to generate the input file for each job
rule generate_input:
    output:
        input_file("{s}", "{N}", "{eta}", "{iteration}")
    shell:
        """
        echo "s={s}, N={N}, eta={eta}, iteration={iteration}" > {output}
        """

# Define the rule to run the program for each job
rule run_program:
    input:
        input_file("{s}", "{N}", "{eta}", "{iteration}")
    output:
        output_file("{s}", "{N}", "{eta}", "{iteration}")
    cluster:
        "sbatch --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=1G --time=0:10:00 --job-name={wildcards.s}_{wildcards.N}_{wildcards.eta}_{wildcards.iteration}"
    shell:
        """
        python run.py --s {wildcards.s} --N {wildcards.N} --eta {wildcards.eta} --iteration {wildcards.iteration} > {output}
        """

# Define the list of all jobs to run
jobs = []
for s in s_values:
    for N in N_values:
        for eta in eta_values:
            for iteration in iteration_values:
                jobs.append((s, N, eta, iteration))

# Define the all rule to run all jobs
rule all:
    input:
        [output_file(s, N, eta, iteration) for s, N, eta, iteration in jobs]

# Define the rule to clean up the output directory
rule clean:
    shell:
        "rm -f output/*"

