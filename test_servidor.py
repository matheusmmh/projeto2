from flask import Flask, request
import mysql.connector
from mysql.connector import Error
from config import config
from unittest.mock import MagicMock, patch
import pytest

with patch("mysql.connector.pooling.MySQLConnectionPool"):
    from servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def existe_imovel(lista, esperado):
    return any(
        all(imovel.get(campo) == valor for campo, valor in esperado.items())
        for imovel in lista
    )
def test_lista_imoveis_retorna_status_200(client):
    response = client.get("/imoveis")
    assert response.status_code == 200

def test_lista_imoveis_retorna_lista_vazia(client):
    imoveis = client.get("/imoveis")
    retorno = imoveis.get_json()
    assert retorno != []

def test_lista_imoveis(client):
    imoveis = client.get("/imoveis")
    imoveis_retornados = imoveis.get_json()
    imoveis_esperados = [
        {'id': 1000, 'logradouro': 'Wheeler Falls', 'tipo_logradouro': 'Avenida', 'bairro': 'Matthewbury', 'cidade': 'New Brandonborough', 'cep': '18235', 'tipo': 'terreno', 'valor': 875932.0, 'data_aquisicao': '2023-01-23'},
        {'id': 812, 'logradouro': 'Jason Club', 'tipo_logradouro': 'Rua', 'bairro': 'Caldwelltown', 'cidade': 'Port Michael', 'cep': '30797', 'tipo': 'terreno', 'valor': 636953.0, 'data_aquisicao': '2020-02-12'},
        {'id': 706, 'logradouro': 'Jessica Burg', 'tipo_logradouro': 'Alameda', 'bairro': 'Lake Sherriland', 'cidade': 'Donaldshire', 'cep': '56944', 'tipo': 'apartamento', 'valor': 180944.0, 'data_aquisicao': '2016-06-04'},
        {'id': 650, 'logradouro': 'Sanchez Unions', 'tipo_logradouro': 'Alameda', 'bairro': 'North Brandon', 'cidade': 'Port Christina', 'cep': '71909', 'tipo': 'casa em condominio', 'valor': 388301.0, 'data_aquisicao': '2017-12-06'},
        {'id': 647, 'logradouro': 'Lori Islands', 'tipo_logradouro': 'Alameda', 'bairro': 'North Beth', 'cidade': 'Jonesport', 'cep': '78411', 'tipo': 'casa em condominio', 'valor': 857538.0, 'data_aquisicao': '2018-05-20'},
    ]

    imoveis_retornados = imoveis.get_json()

    for imovel in imoveis_esperados:
        assert existe_imovel(imoveis_retornados, imovel)

def test_imovel_retorna_status_200(client):
    response = client.get("/imovel/1")
    assert response.status_code == 200

def test_busca_imovel(client):
    imovel_esperado = {
        'id': 1000,
        'logradouro': 'Wheeler Falls',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Matthewbury',
        'cidade': 'New Brandonborough',
        'cep': '18235',
        'tipo': 'terreno',
        'valor': 875932.0,
        'data_aquisicao': '2023-01-23',
    }

    resposta = client.get("/imovel/1000")

    assert resposta.status_code == 200
    assert resposta.get_json() == imovel_esperado

@pytest.mark.parametrize("id_textual", ["id", "abc", "casa", "1000abc", "-texto"])
def test_busca_imovel_id_textual(client, id_textual):
    resposta = client.get(f"/imovel/{id_textual}")

    assert resposta.status_code == 404

def test_busca_imovel_inexistente(client):
    resposta = client.get("/imovel/999999")
    assert resposta.status_code == 404

def test_id_existe(client):
    resposta = client.get("/imovel/1000")
    imovel = resposta.get_json()

    assert resposta.status_code == 200
    assert imovel["id"] == 1000
    assert imovel["id"] > 0

def test_adiciona_imovel():
    return
def test_remove_imovel_existente(client):
    cursor = MagicMock()
    cursor.rowcount = 1

    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    with patch(
        "servidor.db_pool.get_connection",
        return_value=conexao
    ):
        resposta = client.delete("/imovel/1000")

    assert resposta.status_code == 204
    assert resposta.data == b""

def test_remove_imovel_inexistente(client):
    cursor = MagicMock()
    cursor.rowcount = 0

    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    with patch(
        "servidor.db_pool.get_connection",
        return_value=conexao
    ):
        resposta = client.delete("/imovel/999999")

    assert resposta.status_code == 404
    assert resposta.is_json

@pytest.mark.parametrize("id_invalido", ["abc", "-1", "0"])
def test_remove_imovel_id_invalido(client, id_invalido):
    with patch("servidor.db_pool.get_connection") as obter_conexao:
        resposta = client.delete(f"/imovel/{id_invalido}")

    assert resposta.status_code in (400, 422)
    obter_conexao.assert_not_called()

@pytest.mark.parametrize(
    "tipo",
    ["terreno", "apartamento", "casa em condominio"],
)
def test_busca_imoveis_por_tipo(client, tipo):
    cursor = MagicMock()
    cursor.fetchall.return_value = [
        {"id": 1, "cidade": "São Paulo", "tipo": tipo},
    ]

    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    with patch(
        "servidor.db_pool.get_connection",
        return_value=conexao,
    ) as obter_conexao:
        resposta = client.get("/tipo-imovel", query_string={"tipo": tipo})

    assert resposta.status_code == 200
    assert resposta.is_json

    imoveis = resposta.get_json()
    assert isinstance(imoveis, list)
    assert all("tipo" in imovel for imovel in imoveis)

    obter_conexao.assert_called_once_with()
    cursor.execute.assert_called_once()
    consulta, parametros = cursor.execute.call_args.args
    assert "%s" in consulta
    assert tipo not in consulta
    assert parametros == (tipo,)

def test_busca_por_tipo_retorna_apenas_tipo_solicitado(client):
    tipo_solicitado = "terreno"
    cursor = MagicMock()
    cursor.fetchall.return_value = [
        {"id": 1000, "cidade": "New Brandonborough", "tipo": "terreno"},
        {"id": 812, "cidade": "Port Michael", "tipo": "terreno"},
    ]

    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    with patch(
        "servidor.db_pool.get_connection",
        return_value=conexao,
    ):
        resposta = client.get(
            "/tipo-imovel",
            query_string={"tipo": tipo_solicitado},
        )

    assert resposta.status_code == 200
    assert resposta.is_json

    imoveis = resposta.get_json()
    assert isinstance(imoveis, list)
    assert imoveis
    assert all("tipo" in imovel for imovel in imoveis)
    assert all(imovel["tipo"] == tipo_solicitado for imovel in imoveis)

def test_busca_por_tipo_sem_resultados(client):
    cursor = MagicMock()
    cursor.fetchall.return_value = []

    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    with patch(
        "servidor.db_pool.get_connection",
        return_value=conexao,
    ):
        resposta = client.get(
            "/tipo-imovel",
            query_string={"tipo": "apartamento"},
        )

    assert resposta.status_code == 200
    assert resposta.is_json
    assert resposta.get_json() == []
    cursor.execute.assert_called_once()

def test_busca_por_tipo_invalido(client):
    with patch("servidor.db_pool.get_connection") as obter_conexao:
        resposta = client.get(
            "/tipo-imovel",
            query_string={"tipo": "galpao"},
        )

    assert resposta.status_code in (400, 422)
    assert resposta.is_json

    erro = resposta.get_json()
    assert isinstance(erro, dict)
    assert "erro" in erro
    assert isinstance(erro["erro"], str)
    assert erro["erro"].strip()
    obter_conexao.assert_not_called()

def test_busca_por_tipo_ausente(client):
    with patch("servidor.db_pool.get_connection") as obter_conexao:
        resposta = client.get("/tipo-imovel")

    assert resposta.status_code in (400, 422)
    assert resposta.is_json

    erro = resposta.get_json()
    assert isinstance(erro, dict)
    assert "erro" in erro
    assert isinstance(erro["erro"], str)
    assert erro["erro"].strip()
    obter_conexao.assert_not_called()

def test_busca_imovel_tipo():
    return
def test_busca_imovel_cidade():
    return

