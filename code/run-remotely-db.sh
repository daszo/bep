#!/usr/bin/env bash
FILE=""
MESSAGE="routine_update"
ARGS=''
DB="enron.db"

# Loop through all arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
    -f | --file)
        FILE="$2"
        shift
        ;;
    -m | --message)
        MESSAGE="$2"
        shift
        ;;
    -a | --args)
        ARGS="$2"
        shift
        ;;
    -db | --database)
        DB="$2"
        shift
        ;;
    -*)
        echo "Unknown option: $1"
        exit 1
        ;;
    *)
        echo "Invalid: $1. No positional arguments allowed."
        exit 1
        ;;
    esac
    shift
done

# Configuration
REMOTE_USER="daniel"
REMOTE_IP="100.108.63.123" # Your Ubuntu Tailscale IP
PROJECT_DIR='.'
REMOTE_PROJECT_DIR="projects/uva/bep/code" # Folder name
REMOTE_PATH="/home/$REMOTE_USER/$REMOTE_PROJECT_DIR"
# --- Argument Parsing ---
if [ -z ${FILE} ]; then
    echo "Error: Please specify a python file to run."
    echo "Usage: ./run-remotely.sh <script_name.py> [args...]"
    exit 1
fi

git add /home/daszo/uva/bachelor_ki/bep/code/
git commit -m "$MESSAGE"
git push origin main

# 1. Sync Data UP (Arch -> Ubuntu)
echo "Syncing files to Ubuntu..."
rsync -avz ./$PROJECT_DIR/$DB $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/$DB

# 2. Execute Script
echo "Running script on Ubuntu..."
ssh $REMOTE_USER@$REMOTE_IP "
    cd $REMOTE_PATH && \
    git pull && \
    source .venv/bin/activate && \
    python3 $FILE $ARGS"

# 3. Sync Results DOWN (Ubuntu -> Arch)
echo "Retrieving results..."
rsync -avz $REMOTE_USER@$REMOTE_IP:$REMOTE_PATH/$DB ./$PROJECT_DIR/$DB

echo "Done."
