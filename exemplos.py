from config import config
from mysql.connector import pooling
db_pool = pooling.MySQLConnectionPool(
    pool_name="conn",
    pool_size=5,
    **config()
   )

def lista_todos_imoveis():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return

def escolhe_imovel_por_id():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return imoveis
def adiciona_imovel():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return imoveis
def remove_imovel():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return imoveis
def busca_imovel_por_tipo():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return imoveis
    
def busca_imovel_por_cidade():
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM defaultdb.imoveis;")
    imoveis = cursor.fetchall()
    return imoveis

print (lista_todos_imoveis())