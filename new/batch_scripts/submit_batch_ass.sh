#!/bin/bash

# List of files to submit
# FILES=("ass_con.sh" "ass_nco.sh" "ext_con.sh" "ext_nco")
FILES=(
    "ass_05.sh" 
    "ass_05_o.sh" 
    "ass_10.sh" 
    "ass_10_o.sh" 
    "ass_15.sh" 
    "ass_15_o.sh" 
    "ass_20.sh" 
    "ass_20_o.sh" 
    "ass_25.sh" 
    "ass_25_o.sh" 
    "ass_30.sh" 
    "ass_30_o.sh" 
    "ass_40.sh" 
    "ass_40_o.sh" 
    "ass_50.sh" 
    "ass_50_o.sh" 
    "ass_75_o.sh" 
    "ass_75.sh" 
    "ass_100_o.sh" 
    "ass_100.sh" 
)

# Loop through each file and submit using sbatch
for FILE in "${FILES[@]}"; do
    sbatch "$FILE"
    # echo "Submitted $FILE"
done