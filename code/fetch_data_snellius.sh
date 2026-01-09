#!/usr/bin/env bash
DB="validate.N10k_text_rank_d2q_q1.docTquery"
# Configuration
eval $(keychain --eval --agents ssh -Q --quiet $HOME/.ssh/dvoosteroom)

PROJECT_DIR='./data'
REMOTE_PROJECT_DIR="/gpfs/work5/0/prjs1828/DSI-QG/data" # Folder name
REMOTE_PATH="/home/$REMOTE_USER/$REMOTE_PROJECT_DIR"

# 3. Sync Results DOWN (Ubuntu -> Arch)
echo "Retrieving results..."
rsync -avz -e "ssh -4 -i $HOME/.ssh/dvoosteroom" dvoosteroom@snellius.surf.nl:$REMOTE_PROJECT_DIR/$DB ./$PROJECT_DIR/$DB

echo "Done."
