from flask import Flask, request, jsonify

app = Flask(__name__)

'''
Devem haver rotas para:

Listar todos os imóveis com todos os seus atributos;

Listar um imóvel específico pelo seu id com todos os seus atributos;

Adicionar um novo imóvel;

Atualizar um imóvel existente;

Remover um imóvel existente;

Buscar imóveis por tipo (casa, apartamento, terreno, etc) com todos os seus atributos;

Buscar imóveis por cidade com todos os seus atributos;
'''

@app.route("/imoveis", method=["GET"])
def lista_imoveis():
    return

@app.route("/imovel", method=["GET"])
def busca_imovel():
    return

@app.route("/adicionar-imovel", method=["UPDATE"])
def adiciona_imovel():
    return

@app.route("/remover-imovel", method=["DELETE"])
def remove_imovel():
    return

@app.route("/tipo-imovel", method=["GET"])
def busca_tipo_imovel():
    return

@app.route("/cidade-imovel", method=["GET"])
def busca_cidade_imovel():
    return