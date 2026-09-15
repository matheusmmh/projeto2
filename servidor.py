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
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(imoveis),200

@app.route("/imovel", methods=["GET"])
def busca_imovel():
    return

@app.route("/imovel", methods=["POST"])
def adiciona_imovel():
    return

@app.route("/imovel", methods=["DELETE"])
def remove_imovel():
    return

@app.route("/tipo-imovel", methods=["GET"])
def busca_tipo_imovel():
    return

@app.route("/cidade-imovel", methods=["GET"])
def busca_cidade_imovel():
    return