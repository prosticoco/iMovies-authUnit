echo 'installing virtual environment and python dependencies...'
apt-get --assume-yes install python3-venv
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

chmod run +x

. run