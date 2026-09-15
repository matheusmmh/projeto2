from flask import Flask, request, jsonify
from mysql.connector import pooling
from config import config
app = Flask(__name__)

db_pool = pooling.MySQLConnectionPool(
    pool_name="conn",
    pool_size=5,
    **config()
   )

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

@app.route("/imoveis", methods=["GET"])
def lista_imoveis():

    return

@app.route("/imovel", methods=["GET"])
def busca_imovel():
    return

@app.route("/adicionar-imovel", methods=["POST"])
def adiciona_imovel():
    return

@app.route("/remover-imovel", methods=["DELETE"])
def remove_imovel():
    return

@app.route("/tipo-imovel", methods=["GET"])
def busca_tipo_imovel():
    return

@app.route("/cidade-imovel", methods=["GET"])
def busca_cidade_imovel():
    return