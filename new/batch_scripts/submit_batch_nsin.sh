#!/bin/bash

# List of files to submit
# FILES=("ass_con.sh" "ass_nco.sh" "ext_con.sh" "ext_nco")
FILES=(
    "nsin_05.sh" 
    "nsin_05_o.sh" 
    "nsin_10.sh" 
    "nsin_10_o.sh" 
    "nsin_15.sh" 
    "nsin_15_o.sh" 
    "nsin_20.sh" 
    "nsin_20_o.sh" 
    "nsin_25.sh" 
    "nsin_25_o.sh" 
    "nsin_30.sh" 
    "nsin_30_o.sh" 
    "nsin_40.sh" 
    "nsin_40_o.sh" 
    "nsin_50.sh" 
    "nsin_50_o.sh" 
    "nsin_75_o.sh" 
    "nsin_75.sh" 
    "nsin_100_o.sh" 
    "nsin_100.sh" 
)

# Loop through each file and submit using sbatch
for FILE in "${FILES[@]}"; do
    sbatch "$FILE"
    # echo "Submitted $FILE"
done