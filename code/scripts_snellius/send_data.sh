#!/usr/bin/env bash
FILE="${1}"
# Configuration
REMOTE_USER="dvoosteroom"
REMOTE_IP="snellius.surf.nl"
PROJECT_DIR='.'
REMOTE_PROJECT_DIR="/projects/prjs1828"
REMOTE_PATH="$REMOTE_PROJECT_DIR"
#--- Argument Parsing ---
if [ -z ${FILE} ]; then
    echo "Error: supply a file."
    exit 1
fi

eval $(keychain --eval -Q --quiet $HOME/.ssh/dvoosteroom)
# 1. Sync Data UP (Arch -> Ubuntu)
echo "Syncing files to Snellius..."
rsync -avz ./$PROJECT_DIR/$FILE $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/$FILE

# 3. Sync Results DOWN (Ubuntu -> Arch)
# echo "Retrieving results..."
# rsync -avz $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/$DB ./$PROJECT_DIR/$DB

echo "Done."
