#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem-per-cpu=65535
#SBATCH --job-name=MS_11
#SBATCH --mail-type=end
#SBATCH --mail-user=pigo271b@tu-dresden.de

srun --exclusive --ntasks=1 /home/pigo271b/.conda/envs/flexASP/bin/python check_advanced.py 11

echo "waiting for all jobs to complete"
wait
echo "all parallel tasks finished"
