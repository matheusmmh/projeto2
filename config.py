import os
from dotenv import load_dotenv
def config():
    
    load_dotenv('.env')

    return {
        'host': os.getenv('DB_HOST'),  # Obtém o host do banco de dados da variável de ambiente
        'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
        'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
        'database': os.getenv('DB_NAME'),  # Obtém o nome do banco de dados da variável de ambiente
        'port': int(os.getenv('DB_PORT')),  # Obtém a porta do banco de dados da variável de ambiente
        'ssl_ca': os.getenv('SSL_CA_PATH'),  # Caminho para o certificado SSL
    }
