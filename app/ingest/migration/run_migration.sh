#!/bin/bash
set -e

APP_HOME=$(cd ../../../ && pwd)
DB=$APP_HOME/db
MIGRATION=${PWD}
DATA=$MIGRATION/data

#Clean out old data
rm $DB/rabpubs.db
rm $DATA/*.csv

# SQLite setup
python $DB/write_db.py $DB

# Break old DB data into multiple CSVs
python $MIGRATION/convert_existing_tsv.py $DATA $DATA/pubs.tsv

# Convert CSVs and load into Flask SQLite DB
python $MIGRATION/load_users_and_sources.py $DATA/users.csv
python $MIGRATION/load_events_and_exids.py $DATA/hrv_exids.csv