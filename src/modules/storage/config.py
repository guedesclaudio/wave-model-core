import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do MinIO
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'false').lower() == 'true'

# Verificação de configurações obrigatórias
if not MINIO_ACCESS_KEY:
    raise ValueError("MINIO_ACCESS_KEY não está definido nas variáveis de ambiente")

if not MINIO_SECRET_KEY:
    raise ValueError("MINIO_SECRET_KEY não está definido nas variáveis de ambiente")

if not MINIO_BUCKET_NAME:
    raise ValueError("MINIO_BUCKET_NAME não está definido nas variáveis de ambiente") 