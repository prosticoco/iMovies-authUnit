#!/bin/bash
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
chmod u+x run
. run