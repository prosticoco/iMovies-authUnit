#!/bin/bash

DB_ROOT_PASSWORD=$1
DUMP_PATH=$1


chmod u+x scripts/virtualenvsetup.sh 

echo 'installing mySQL server'
sh scripts/install_mysql.sh $DB_ROOT_PASSWORD 
echo 'Setting up database'
echo 'PATH in install only'
echo $DUMP_PATH
sh scripts/setup_mysql.sh $DB_ROOT_PASSWORD $DUMP_PATH
DB_ROOT_PASSWORD=$1
echo 'updating system'
apt-get update --fix-missing
echo 'installing virtual environment and python dependencies...'
echo 'installing venv'
apt-get --assume-yes install python3-venv
python3 -m venv venv
echo 'activating environment'
source venv/bin/activate
echo 'installing requirements'
pip install -r requirements.txt
pip install -r requirements.txt
#echo 'creating dedicated user'
#useradd -c 'Bobby Daemon' -m bob
#echo 'choose dedicated user password'
#echo "bob:1234" | chpasswd --encrypted

chmod u+x run

