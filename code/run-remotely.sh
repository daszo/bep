#!/bin/bash

# Configuration
REMOTE_USER="daniel"
REMOTE_IP="100.108.63.123"          # Your Ubuntu Tailscale IP
PROJECT_DIR="projects/uva/bep/code" # Folder name
REMOTE_PATH="/home/$REMOTE_USER/$PROJECT_DIR"

# 1. Sync Data UP (Arch -> Ubuntu)
echo "Syncing files to Ubuntu..."
rsync -avz --exclude '.git' ./$PROJECT_DIR/ $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/

# 2. Execute Script
echo "Running script on Ubuntu..."
ssh $REMOTE_USER@$REMOTE_IP "cd $REMOTE_PATH && python3 train.py"

# 3. Sync Results DOWN (Ubuntu -> Arch)
# Assuming your python script saves output to an 'output' folder
echo "Retrieving results..."
rsync -avz $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/output/ ./$PROJECT_DIR/output/

echo "Done."
