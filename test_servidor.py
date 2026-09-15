from flask import Flask, request
import mysql.connector
from mysql.connector import Error
from config import config
from unittest.mock import MagicMock, patch
from servidor import app
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()
#caso alguma função tenha que olhar campos especificos
def existe_imovel(lista,esperado):
    return any(all(imovel.get(campo) == valor
                   for campo, valor in esperado.items()) 
                for imovel in lista)

def test_lista_imoveis(client):
    imoveis = client.get("/imoveis")

    assert imoveis.status_code == 200

    imoveis_retornados = imoveis.json
    imoveis_esperados = [
        {'id': 1000, 'logradouro': 'Wheeler Falls', 'tipo_logradouro': 'Avenida', 'bairro': 'Matthewbury', 'cidade': 'New Brandonborough', 'cep': '18235', 'tipo': 'terreno', 'valor': 875932.0, 'data_aquisicao': '2023-01-23'},
        {'id': 812, 'logradouro': 'Jason Club', 'tipo_logradouro': 'Rua', 'bairro': 'Caldwelltown', 'cidade': 'Port Michael', 'cep': '30797', 'tipo': 'terreno', 'valor': 636953.0, 'data_aquisicao': '2020-02-12'},
        {'id': 706, 'logradouro': 'Jessica Burg', 'tipo_logradouro': 'Alameda', 'bairro': 'Lake Sherriland', 'cidade': 'Donaldshire', 'cep': '56944', 'tipo': 'apartamento', 'valor': 180944.0, 'data_aquisicao': '2016-06-04'},
        {'id': 650, 'logradouro': 'Sanchez Unions', 'tipo_logradouro': 'Alameda', 'bairro': 'North Brandon', 'cidade': 'Port Christina', 'cep': '71909', 'tipo': 'casa em condominio', 'valor': 388301.0, 'data_aquisicao': '2017-12-06'},
        {'id': 647, 'logradouro': 'Lori Islands', 'tipo_logradouro': 'Alameda', 'bairro': 'North Beth', 'cidade': 'Jonesport', 'cep': '78411', 'tipo': 'casa em condominio', 'valor': 857538.0, 'data_aquisicao': '2018-05-20'}
    ]
    for esperado in imoveis_esperados:
        assert existe_imovel(imoveis_retornados, esperado)
    
def test_busca_imovel():
    return

def novo_imovel_valido():
    return {
        "logradouro": "Rua das Flores",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01000-000",
        "tipo": "apartamento",
        "valor": 500000.0,
        "data_aquisicao": "2026-09-15"
    }


@patch("servidor.db_pool")
def test_adiciona_imovel_valido(mock_pool, client):
    resposta = client.post("/adicionar-imovel", json=novo_imovel_valido())

    assert resposta.get_json()["mensagem"] == "Imóvel adicionado com sucesso"


@patch("servidor.db_pool")
def test_adiciona_imovel_retorna_status_201(mock_pool, client):
    resposta = client.post("/adicionar-imovel", json=novo_imovel_valido())

    assert resposta.status_code == 201


@patch("servidor.db_pool")
def test_adiciona_imovel_retorna_id(mock_pool, client):
    cursor = mock_pool.get_connection.return_value.cursor.return_value
    cursor.lastrowid = 1001

    resposta = client.post("/adicionar-imovel", json=novo_imovel_valido())

    assert resposta.get_json()["id"] == 1001


@patch("servidor.db_pool")
def test_adiciona_imovel_sem_campo_obrigatorio(mock_pool, client):
    imovel = novo_imovel_valido()
    del imovel["logradouro"]

    resposta = client.post("/adicionar-imovel", json=imovel)

    assert resposta.status_code == 400


@patch("servidor.db_pool")
def test_adiciona_imovel_com_valor_negativo(mock_pool, client):
    imovel = novo_imovel_valido()
    imovel["valor"] = -1

    resposta = client.post("/adicionar-imovel", json=imovel)

    assert resposta.status_code == 400


@patch("servidor.db_pool")
def test_adiciona_imovel_com_tipo_invalido(mock_pool, client):
    imovel = novo_imovel_valido()
    imovel["tipo"] = "castelo"

    resposta = client.post("/adicionar-imovel", json=imovel)

    assert resposta.status_code == 400


@patch("servidor.db_pool")
def test_adiciona_imovel_erro_no_banco(mock_pool, client):
    cursor = mock_pool.get_connection.return_value.cursor.return_value
    cursor.execute.side_effect = Error("Erro simulado no banco")

    resposta = client.post("/adicionar-imovel", json=novo_imovel_valido())

    assert resposta.status_code == 500

def test_remove_imovel():
    return
def test_busca_imovel_tipo():
    return
def test_busca_imovel_cidade():
    return

