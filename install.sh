#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install flask
chmod a+x scrip_end_server.sh
source script_end_server.sh
./app.py