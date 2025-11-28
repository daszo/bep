#!/bin/bash

# Configuration
REMOTE_USER="daniel"
REMOTE_IP="100.108.63.123" # Your Ubuntu Tailscale IP
PROJECT_DIR='.'
REMOTE_PROJECT_DIR="projects/uva/bep/code" # Folder name
REMOTE_PATH="/home/$REMOTE_USER/$REMOTE_PROJECT_DIR"
# --- Argument Parsing ---
if [ -z "$1" ]; then
    echo "Error: Please specify a python file to run."
    echo "Usage: ./run-remotely.sh <script_name.py> [args...]"
    exit 1
fi

FIRST_ARG="$1"     # The first argument
REST_ARGS="${@:2}" # All arguments starting from the 2nd one

# 1. Sync Data UP (Arch -> Ubuntu)
# echo "Syncing files to Ubuntu..."
rsync -avz ./$PROJECT_DIR/enron.db $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/enron.db

# 2. Execute Script
echo "Running script on Ubuntu..."
ssh $REMOTE_USER@$REMOTE_IP "cd $REMOTE_PATH && python3 $FIRST_ARG $REST_ARGS"

# 3. Sync Results DOWN (Ubuntu -> Arch)
# Assuming your python script saves output to an 'output' folder
echo "Retrieving results..."
rsync -avz $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/output/ ./$PROJECT_DIR/output/

echo "Done."
