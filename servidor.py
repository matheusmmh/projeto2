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

@app.route("/imovel/<int:id>", methods=["GET"])
def busca_imovel(id):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    imovel = cursor.fetchone()

    cursor.close()
    conn.close()
    if imovel is None:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    return jsonify(imovel),200

@app.route("/adicionar-imovel", methods=["POST"])
def adiciona_imovel():
    dados = request.get_json()

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

    # Verifica se todos os campos foram enviados
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

    # Verifica o tipo do imóvel
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

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Imóvel adicionado com sucesso",
            "id": id_imovel
        }), 201

    except Exception:
        return jsonify({
            "erro": "Erro ao adicionar imóvel"
        }), 500

@app.route("/imovel/<int:id>", methods=["DELETE"])
def remove_imovel():
    return

@app.route("/tipo-imovel", methods=["GET"])
def busca_tipo_imovel():
    return

@app.route("/cidade-imovel", methods=["GET"])
def busca_cidade_imovel():
    return