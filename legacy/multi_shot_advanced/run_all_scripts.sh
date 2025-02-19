#!/bin/bash

# Set the directory path
DIR="./scripts"

# Loop through all files in the directory
for file in $DIR/*
do
  # Check if the file is a regular file
  if [ -f "$file" ]
  then
    # Submit job
    sbatch $file
  fi
done