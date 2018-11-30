from flask import Flask, request
import requests
import os


app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):

    print('entrou catch all')
    
    ip = os.environ.get('IPBANCO')

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