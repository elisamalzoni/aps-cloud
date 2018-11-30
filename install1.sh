#!/bin/bash
sudo apt update
# sudo apt install -y python3-pip
pip3 install flask
pip3 install boto3
python3 db_instance.py
python3 lb.py
