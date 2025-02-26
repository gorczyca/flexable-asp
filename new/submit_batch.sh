#!/bin/bash

# List of files to submit
FILES=("run_iassc.sh" "run_iassn.sh" "run_iextc.sh" "run_iextn.sh")

# Loop through each file and submit using sbatch
for FILE in "${FILES[@]}"; do
    sbatch "$FILE"
    echo "Submitted $FILE"
done