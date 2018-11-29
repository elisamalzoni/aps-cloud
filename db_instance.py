from flask import Flask, request, jsonify
from tarefac import Tarefa
import boto3
from pprint import pprint
import random
import requests
import numpy as np
import threading
import time

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def cria_instancia(ec2, n):
    
    instances = ec2.create_instances(
        ImageId='ami-0ac019f4fcb7cb7e6', # image id ubuntu 18 ami-0ac019f4fcb7cb7e6
        MinCount=n,
        MaxCount=n,
        InstanceType='t2.micro',
        KeyName='elisaaps',
        SecurityGroups=[
            'elisasc',
        ],
        UserData='''#!/bin/bash
                    cd /home/ubuntu
                    git clone https://github.com/elisamalzoni/aps-cloud.git
                    cd aps-cloud
                    chmod a+x install.sh
                    ./install.sh''',
        TagSpecifications=[
            {   'ResourceType': 'instance',
                'Tags':[
                    {
                        'Key': 'Owner',
                        'Value': 'elisabanco'
                    },
                ]
            },
        ]
    )
cria_instancia(ec2, 1)