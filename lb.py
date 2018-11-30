#!/usr/bin/python3

from flask import Flask, request
import boto3
from pprint import pprint
import random
import requests
import numpy as np
import threading
import time

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

app = Flask(__name__)

def randon_ip(dici):
    ips = [i for i in dici.keys()]
    rand = np.random.choice(ips)
    return dici[rand]

def instancias_rodando(client):
    maq_rodando = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'elisa',
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ],
    )

    dici_ips = {}

    for i in maq_rodando['Reservations']:
        for c in i['Instances']:
            dici_ips[c['InstanceId']] = c['PublicIpAddress']
        
    return dici_ips




def cria_instancia(ec2, n, ipbanc):

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
                    export IPBANCO={}
                    chmod a+x installlb.sh
                    ./installlb.sh'''.format(ipbanc),
        TagSpecifications=[
            {   'ResourceType': 'instance',
                'Tags':[
                    {
                        'Key': 'Owner',
                        'Value': 'elisa'
                    },
                ]
            },
        ]
    )

def apaga_intancia(client, ids_list):
    response = client.terminate_instances(
        InstanceIds=ids_list
    )

dici_ips = instancias_rodando(client)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    print('entrou catch all')
    red = randon_ip(dici_ips)

    ende = 'http://'+red+':5000/'+path
    print(ende)
    if request.method == 'GET':
        r = requests.get(ende)
        print(r.text)
        return r.text

    elif request.method == 'POST':
        j = request.json
        r = requests.post(ende, json=j)
        print(r.text)
        return r.text

    elif request.method == 'PUT':
        j = request.json
        r = requests.put(ende, json=j)
        print(r.text)
        return r.text

    elif request.method == 'DELETE':
        r = requests.delete(ende)
        print(r.text)
        return r.text


def hcloop(dici_ips, client, ec2, n, ipbanc):
    

    while True:
        print('-------------------------------------')
        dici_ips = instancias_rodando(client)
        if len(dici_ips.values())>n:
            # print('n: {}'.format(n))
            deletar = len(dici_ips.values()) - n
            for i, (k, v) in enumerate(dici_ips.items()):
                if i <= deletar:
                    print('deletando {}/{}'.format(i+1,deletar))
                    apaga_intancia(client, [k])
                    time.sleep(120)

        elif len(dici_ips.values())<n:
            criar = n - len(dici_ips.values())
            print('criando {} novas instancias'.format(criar))
            cria_instancia(ec2, criar, ipbanc)
            time.sleep(120)

        for id_i, ip in dici_ips.items():
            end = 'http://{}:5000/healthcheck'.format(ip)
            print('endereco: ', end)
            try:
                r = requests.get(end, timeout=20)
                if r.status_code != 200:
                    apaga_intancia(client, [id_i])
                    print('apagando instancia: ', id_i)
                    ## contador timeout ???
                    time.sleep(120)
                    cria_instancia(ec2, 1, ipbanc)

            except:
                apaga_intancia(client, [id_i])
                print('apagando instancia: ', id_i)
                ## contador timeout ???
                print('{} entrou timeout'.format(end))
                cria_instancia(ec2, 1, ipbanc)
                time.sleep(120)

        time.sleep(3)

def get_ip_banco():

    banco = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'elisabanco',
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ],
    )
    ipb = 0
    for i in banco['Reservations']:
        for c in i['Instances']:
            ipb = c['PublicIpAddress']
    return ipb

def cria_db(ec2, n):
    
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


cria_db(ec2, 1)
print('criando banco de dados....')
time.sleep(50)
print('ip banco:', get_ip_banco())

if __name__ == '__main__':

    t = threading.Thread(target=hcloop(dici_ips, client, ec2, 4, get_ip_banco()))
    t.start()
    app.run(debug=True, host='0.0.0.0')