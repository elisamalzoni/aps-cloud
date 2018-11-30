#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install flask
pip3 install boto3
pip3 install numpy
cd /home/ubuntu
git clone https://github.com/elisamalzoni/aps-cloud.git
cd aps-cloud
python3 lb.py
