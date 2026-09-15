from flask import Flask, request
import mysql.connector
from mysql.connector import Error
from config import config
from unittest.mock import MagicMock, patch
from servidor import app

def client():
    app.config["TESTING"] = True
    return app.test_client()
#caso alguma função tenha que olhar campos especificos
def existe_imovel(lista,esperado):
    return any(all(imovel.get(campo) == valor for campo, valor in esperado.items() 
                   for imovel in lista))

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
    for imovel in imoveis_esperados[-1]:
        assert imovel in imoveis_esperados
    
def test_busca_imovel():
    return
def test_adiciona_imovel():
    return
def test_remove_imovel():
    return
def test_busca_imovel_tipo():
    return
def test_busca_imovel_cidade():
    return

