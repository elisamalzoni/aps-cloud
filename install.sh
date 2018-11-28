#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install flask
source ./script_end_server.sh
./app.py