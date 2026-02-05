#!/usr/bin/env bash

PROJECT_DIR='./data'
REMOTE_PROJECT_DIR="/gpfs/work5/0/prjs1828/DSI-QG/" # Folder name

download_file() {

    local from="$REMOTE_PROJECT_DIR/$1"
    local to="$PROJECT_DIR/$2"

    echo "Retrieving results... $from to $to"

    rsync -avz -e "ssh -4 -i $HOME/.ssh/dvoosteroom" dvoosteroom@snellius.surf.nl:$from $to

    echo "Done."

}
# Configuration
eval $(keychain --eval --agents ssh -Q --quiet $HOME/.ssh/dvoosteroom)
download_file "indexes/enron_index_N10k/test.N10k.docTquery.bm25_debug_logs.csv" "bm25_10k_no_thread_results.csv"
download_file "indexes/enron_index_N10k_thread_same_mid/test.N10k_thread_same_mid.docTquery.bm25_debug_logs.csv" "bm25_10k_thread_same_mid_results.csv"
download_file "indexes/enron_index_N10k_thread/test.N10k_thread.docTquery.bm25_debug_logs.csv" "bm25_10k_thread_results.csv"
download_file "indexes/enron_index_N100k_thread/test.N100k_thread.docTquery.bm25_debug_logs.csv" "bm25_100k_thread_results.csv"

dir="data_logs"
download_file "$dir/test.N10k.docTquery.dsi_inference_debug_logs.csv" "dsi_10k_no_thread_results.csv"
download_file "$dir/test.N10k_thread_same_mid.docTquery.dsi_inference_debug_logs.csv" "dsi_10k_thread_same_mid_results.csv"
download_file "$dir/test.N10k_thread.docTquery.dsi_inference_debug_logs.csv" "dsi_10k_thread_results.csv"
download_file "$dir/test.N100k_thread.docTquery.dsi_inference_debug_logs.csv" "dsi_100k_thread_results.csv"
