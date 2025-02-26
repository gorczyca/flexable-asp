#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem-per-cpu=65535
#SBATCH --mail-type=end
#SBATCH --mail-user=pigo271b@tu-dresden.de

sbatch --job-name=IncAssC /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python run_test.py assumptions True
sbatch --job-name=IncAssNC /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python run_test.py assumptions False
sbatch --job-name=IncExtC /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python run_test.py externals True
sbatch --job-name=IncExtNC /data/horse/ws/pigo271b-flexasp-workspace/.conda/envs/flexable/bin/python run_test.py externals False

echo "Jobs submitted independently."
