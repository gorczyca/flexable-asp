#!/bin/bash

# List of files to submit
# FILES=("ass_con.sh" "ass_nco.sh" "ext_con.sh" "ext_nco")
FILES=(
    "ext_05.sh" 
    "ext_05_o.sh" 
    "ext_10.sh" 
    "ext_10_o.sh" 
    "ext_15.sh" 
    "ext_15_o.sh" 
    "ext_20.sh" 
    "ext_20_o.sh" 
    "ext_25.sh" 
    "ext_25_o.sh" 
    "ext_30.sh" 
    "ext_30_o.sh" 
    "ext_40.sh" 
    "ext_40_o.sh" 
    "ext_50.sh" 
    "ext_50_o.sh" 
    "ext_75_o.sh" 
    "ext_75.sh" 
    "ext_100_o.sh" 
    "ext_100.sh" 
)

# Loop through each file and submit using sbatch
for FILE in "${FILES[@]}"; do
    sbatch "$FILE"
    # echo "Submitted $FILE"
done