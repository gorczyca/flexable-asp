#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem-per-cpu=65535
#SBATCH --job-name=ass_con
#SBATCH --mail-type=end
#SBATCH --mail-user=pigo271b@tu-dresden.de


srun --exclusive --ntasks=1 /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python /data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/run_initially_aspforaba.py -a aspforaba 

echo "waiting for all jobs to complete"
wait
echo "all parallel tasks finished"
