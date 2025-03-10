#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem-per-cpu=65535
#SBATCH --job-name=nsin_5_o
#SBATCH --mail-type=end
#SBATCH --mail-user=pigo271b@tu-dresden.de

srun --exclusive --ntasks=1 /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python /data/horse/ws/pigo271b-flexasp-workspace/flexable-asp/new/run_test.py -a naive_singleshot -x 5 -o

echo "waiting for all jobs to complete"
wait
echo "all parallel tasks finished"
