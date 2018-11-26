#!/usr/bin/python3

from flask import Flask, request, jsonify
from tarefac import Tarefa

app = Flask(__name__)

id_count = 0
dic_tarefas = {} # id: objeto tarefa

dic_tarefas[id_count] = Tarefa('tituloooo', 'desa dmasd', False)
id_count += 1
dic_tarefas[id_count] = Tarefa('aloos', 'alod', True)

id_count += 1
dic_tarefas[id_count] = Tarefa('descomp', 'estudar pra prova', False)


@app.route('/Tarefa', methods=['GET', 'POST'])
def taref():
    if not request.json or not 'title' in request.json:
        abort(400)
    global id_count, dic_tarefas
    if request.method == 'GET':
        tarefas = []
        for k, v in dic_tarefas.items():
            t = "titulo: " + v.get_title()
            d = "descricao: " + v.get_description()
            s = "feita: " + str(v.get_done())
            tarefas.append([t,d,s])
        return jsonify(tarefas)
    else:
        t = request.json.get('title')
        d = request.json.get('description')
        s = request.json.get('done')
        tar = Tarefa(t, d, s)
        dic_tarefas[id_count+1] = tar
        id_count += 1

        tarefas = []
        for k, v in dic_tarefas.items():
            t = "titulo: " + v.get_title()
            d = "descricao: " + v.get_description()
            s = "feita: " + str(v.get_done())
            tarefas.append([t,d,s])
        return jsonify(tarefas), 201

@app.route('/Tarefa/<int:tarefa_id>', methods=['GET', 'PUT', 'DELETE'])
def taref_id(tarefa_id):
    try:
        if request.method == 'GET':
            ta = dic_tarefas[tarefa_id]
            t = "titulo: " + ta.get_title()
            d = "descricao: " + ta.get_description()
            s = "feita: " + str(ta.get_done())
            return jsonify([t,d,s])

        elif request.method == 'PUT':
            ta = dic_tarefas[tarefa_id]
            ta.set_title(request.json.get('title')
            ta.set_description(request.json.get('description')
            ta.set_done(request.json.get('done')
            t = "titulo: " + ta.get_title()
            d = "descricao: " + ta.get_description()
            s = "feita: " + str(ta.get_done())
            return jsonify([t,d,s]), 200
        
        elif request.method == 'DELETE':
            del dic_tarefas[tarefa_id]
            return '200'
    except:
        return '404'

@app.route('/healthcheck')
def hc():
    return '200'

if __name__ == '__main__':
    app.run(debug=True)