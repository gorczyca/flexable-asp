#!/bin/bash

# Start a new tmux session named "mysession" and detach
tmux new-session -d -s mysession

# Split window into left and right panes
tmux split-window -h

# Split the left pane into top and bottom
tmux select-pane -t 0
tmux split-window -v

# Split the right pane into top and bottom
tmux select-pane -t 2
tmux split-window -v

# Run different commands in each pane
tmux send-keys -t 0 "conda activate flexable; python run_test.py assumptions True; tmux clock-mode" C-m


tmux send-keys -t 1 "conda activate flexable; python run_test.py assumptions False; tmux clock-mode" C-m


tmux send-keys -t 2 "conda activate flexable; python run_test.py externals True; tmux clock-mode" C-m


tmux send-keys -t 3 "conda activate flexable; python run_test.py externals False; tmux clock-mode" C-m

# Attach to the tmux session
tmux attach -t mysession
