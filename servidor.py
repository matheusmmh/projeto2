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
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imoveis")
        imoveis = cursor.fetchall()
        return jsonify(imoveis), 200
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

@app.route("/imovel/<int:id>", methods=["GET"])
def busca_imovel(id):
    conn = db_pool.get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
        imovel = cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    if imovel is None:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    return jsonify(imovel), 200

@app.route("/adicionar-imovel", methods=["POST"])
def adiciona_imovel():
    dados = request.get_json(silent=True)

    campos = [
        "logradouro",
        "tipo_logradouro",
        "bairro",
        "cidade",
        "cep",
        "tipo",
        "valor",
        "data_aquisicao"
    ]

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido"}), 400


    for campo in campos:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} é obrigatório"
            }), 400

    # Verifica o valor do imóvel
    if dados["valor"] < 0:
        return jsonify({
            "erro": "O valor não pode ser negativo"
        }), 400

    tipos_validos = [
        "casa",
        "apartamento",
        "terreno",
        "casa em condominio"
    ]

    if dados["tipo"] not in tipos_validos:
        return jsonify({
            "erro": "Tipo de imóvel inválido"
        }), 400

    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        comando = """
            INSERT INTO imoveis (
                logradouro,
                tipo_logradouro,
                bairro,
                cidade,
                cep,
                tipo,
                valor,
                data_aquisicao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            dados["logradouro"],
            dados["tipo_logradouro"],
            dados["bairro"],
            dados["cidade"],
            dados["cep"],
            dados["tipo"],
            dados["valor"],
            dados["data_aquisicao"]
        )

        cursor.execute(comando, valores)
        conn.commit()

        id_imovel = cursor.lastrowid

        return jsonify({
            "mensagem": "Imóvel adicionado com sucesso",
            "id": id_imovel
        }), 201

    except Exception:
        return jsonify({
            "erro": "Erro ao adicionar imóvel"
        }), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route("/imovel/<id>", methods=["DELETE"])
def remove_imovel(id):
    # Verifica se o ID é um número positivo
    if not id.isdigit() or int(id) <= 0:
        return jsonify({"erro": "ID do imóvel inválido"}), 400

    id = int(id)

    conn = db_pool.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))

    # rowcount mostra quantos imóveis foram removidos
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    conn.commit()
    cursor.close()
    conn.close()

    # O status 204 deve ser retornado sem conteúdo
    return "", 204

@app.route("/imovel/<id>", methods=["GET"])
def busca_imovel_id_invalido(id):
    return jsonify({"erro": "Imóvel não encontrado"}), 404

@app.route("/tipo-imovel", methods=["GET"])
def busca_tipo_imovel():
    tipo = request.args.get("tipo")
    tipos_validos = {
        "terreno",
        "apartamento",
        "casa",
        "casa em condominio",
    }

    if tipo not in tipos_validos:
        return jsonify({"erro": "Tipo de imovel invalido"}), 400

    conn = db_pool.get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM imoveis WHERE tipo = %s",
            (tipo,),
        )
        imoveis = cursor.fetchall()
        return jsonify(imoveis), 200
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

@app.route("/cidade-imovel", methods=["GET"])
def busca_cidade_imovel():
    cidade = request.args.get("cidade")

    if cidade is None or not cidade.strip():
        return jsonify({"erro": "Cidade obrigatoria"}), 400

    conn = db_pool.get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM imoveis WHERE cidade = %s",
            (cidade,),
        )
        imoveis = cursor.fetchall()
        return jsonify(imoveis), 200
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()
