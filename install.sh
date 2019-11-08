#!/bin/bash

DB_ROOT_PASSWORD=$1
DUMP_PATH=$2

sh scripts/install_mysql.sh $DB_ROOT_PASSWORD 
sh scripts/setup_mysql.sh $DB_ROOT_PASSWORD $DUMP_PATH

pip install -r requirements.txt

chmod run +x

