#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem-per-cpu=65535
#SBATCH --job-name=MS_{{}}
#SBATCH --mail-type=end
#SBATCH --mail-user=pigo271b@tu-dresden.de

srun --exclusive --ntasks=1 /home/pigo271b/.conda/envs/flexASP/bin/python check_with_asp_alt_strat.py {{}}

echo "waiting for all jobs to complete"
wait
echo "all parallel tasks finished"
