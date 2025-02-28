#!/bin/bash

# List of files to submit
# FILES=("ass_con.sh" "ass_nco.sh" "ext_con.sh" "ext_nco")
FILES=(
    "sin_5.sh" 
    "sin_5_s.sh" 
    "sin_10.sh" 
    "sin_10_s.sh" 
    "sin_15.sh" 
    "sin_15_s.sh" 
    "sin_20.sh" 
    "sin_20_s.sh" 
    "sin_25.sh" 
    "sin_25_s.sh" 
    "sin_30.sh" 
    "sin_30_s.sh" 
    "sin_50.sh" 
    "sin_50_s.sh" 
    "sin_75.sh" 
    "sin_75_s.sh" 
    "sin_100.sh" 
    "sin_100_s.sh" 
)

# Loop through each file and submit using sbatch
for FILE in "${FILES[@]}"; do
    sbatch "$FILE"
    # echo "Submitted $FILE"
done