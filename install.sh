sudo apt update
sudo apt install -y python3-pip
pip3 install flask
cd ~/aps-cloud
source ./script_end_server.sh
./app.py