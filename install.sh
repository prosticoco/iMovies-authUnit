#!/bin/bash

DB_ROOT_PASSWORD=$1
DUMP_PATH=$2


#apt-get update
#apt-get upgrade
chmod scripts/virtualenvsetup.sh u+x

echo 'installing mySQL server'
sh scripts/install_mysql.sh $DB_ROOT_PASSWORD 
echo 'Setting up database'
sh scripts/setup_mysql.sh $DB_ROOT_PASSWORD $DUMP_PATH

./scripts/virtualenvsetup

