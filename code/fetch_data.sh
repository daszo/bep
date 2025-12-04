#!/usr/bin/env bash
DB="N10k_text_rank_msmarco.tsv"
# Configuration
REMOTE_USER="daniel"
REMOTE_IP="100.108.63.123" # Your Ubuntu Tailscale IP
PROJECT_DIR='./data'
REMOTE_PROJECT_DIR="projects/uva/bep/code/data" # Folder name
REMOTE_PATH="/home/$REMOTE_USER/$REMOTE_PROJECT_DIR"

# 3. Sync Results DOWN (Ubuntu -> Arch)
echo "Retrieving results..."
rsync -avz $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/$DB ./$PROJECT_DIR/$DB

echo "Done."
