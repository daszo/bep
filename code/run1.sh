#!/usr/bin/env bash

./run-remotely-db.sh -f clean_files.py

sqlite3 enron.db <sql/drop_folders.sql
sqlite3 enron.db <sql/cleaned_view.sql
