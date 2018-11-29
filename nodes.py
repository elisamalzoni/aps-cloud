from flask import Flask, request
import boto3
import requests

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

app = Flask(__name__)
def ip_banco(client):
    maq_rodando = client.describe_instances(
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

    dici_ips = {}

    for i in maq_rodando['Reservations']:
        for c in i['Instances']:
            ip = c['PublicIpAddress']
        
    return ip

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):

    print('entrou catch all')
    
    ip = ip_banco(client)

    ende = 'http://'+ip+':5000/'+path
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

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')