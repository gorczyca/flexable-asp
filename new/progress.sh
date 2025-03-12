#!/bin/bash

FOLDER="results"  # Change this to your actual folder path
TOTAL=6800

for file in "$FOLDER"/*; do
    if [[ -f "$file" ]]; then
        lowest_id=$(tail -n 1 "$file" | cut -d, -f1)
        
        if [[ "$lowest_id" -ne 6800 ]]; then
            percentage=$((lowest_id * 100 / TOTAL))
            echo "$(basename "$file"): $lowest_id [$percentage%]"
        fi
    fi
done

