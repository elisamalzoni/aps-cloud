#!/usr/bin/python3

import sys
import requests
import json
import os


var = os.environ.get('END')
end = str(var)
print('endereco: ', end)

if sys.argv[1] == 'adicionar':
    t = sys.argv[2]
    d = sys.argv[3]
    s = sys.argv[4]
    h = {'content-type': 'application/json'}
    dp = {'title': t, 'description': d, 'done': s}
    r = requests.post(end + '/Tarefa', data=json.dumps(dp), headers=h)
    print(r.text)

elif sys.argv[1] == 'listar':
    r = requests.get(end + '/Tarefa')
    print(r.text)

elif sys.argv[1] == 'buscar':
    t_id = sys.argv[2]
    r = requests.get(end + '/Tarefa/' + t_id)
    print(r.text)



elif sys.argv[1] == 'apagar':
    t_id = sys.argv[2]
    r = requests.delete(end + '/Tarefa/' + t_id)
    print(r.text)

elif sys.argv[1] == 'atualizar':
    t_id = sys.argv[2]
    t = sys.argv[3]
    d = sys.argv[4]
    s = sys.argv[5]
    h = {'content-type': 'application/json'}
    dp = {'title': t, 'description': d, 'done': s}
    r = requests.put(end + '/Tarefa/'+ t_id, data=json.dumps(dp), headers=h)
    print(r.text)

