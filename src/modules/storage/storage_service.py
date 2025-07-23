from minio import Minio
from minio.error import S3Error
from typing import Optional, List
import os
from .config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_BUCKET_NAME

class StorageService:
    def __init__(self):
        """
        Inicializa o serviço de armazenamento do MinIO.
        
        Args:
            bucket_name (str): Nome do bucket do MinIO
        """
        self.client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        self.bucket_name = MINIO_BUCKET_NAME
        
        # Cria o bucket se não existir
        if not self.client.bucket_exists(MINIO_BUCKET_NAME):
            self.client.make_bucket(MINIO_BUCKET_NAME)
    
    def upload_file(self, source_file_path: str, destination_blob_name: str) -> str:
        """
        Faz upload de um arquivo para o MinIO.
        
        Args:
            source_file_path (str): Caminho local do arquivo
            destination_blob_name (str): Nome do arquivo de destino no bucket
            
        Returns:
            str: URL pública do arquivo enviado
        """
        self.client.fput_object(
            bucket_name=self.bucket_name,
            object_name=destination_blob_name,
            file_path=source_file_path
        )
        
        return self.get_file_url(destination_blob_name)
    
    def download_file(self, source_blob_name: str, destination_file_path: str) -> None:
        """
        Faz download de um arquivo do MinIO.
        
        Args:
            source_blob_name (str): Nome do arquivo no bucket
            destination_file_path (str): Caminho local onde o arquivo será salvo
        """
        self.client.fget_object(
            bucket_name=self.bucket_name,
            object_name=source_blob_name,
            file_path=destination_file_path
        )
    
    def get_file_url(self, blob_name: str) -> str:
        """
        Gera a URL pública de um arquivo.
        
        Args:
            blob_name (str): Nome do arquivo no bucket
            
        Returns:
            str: URL pública do arquivo
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=blob_name
            )
            return url
        except S3Error:
            return ""
    
    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        Lista todos os arquivos no bucket.
        
        Args:
            prefix (str, optional): Prefixo para filtrar arquivos
            
        Returns:
            List[str]: Lista com os nomes dos arquivos
        """
        objects = self.client.list_objects(
            bucket_name=self.bucket_name,
            prefix=prefix or ""
        )
        return [obj.object_name for obj in objects]
    
    def delete_file(self, blob_name: str) -> None:
        """
        Deleta um arquivo do bucket.
        
        Args:
            blob_name (str): Nome do arquivo a ser deletado
        """
        self.client.remove_object(
            bucket_name=self.bucket_name,
            object_name=blob_name
        )
    
    def file_exists(self, blob_name: str) -> bool:
        """
        Verifica se um arquivo existe no bucket.
        
        Args:
            blob_name (str): Nome do arquivo a ser verificado
            
        Returns:
            bool: True se o arquivo existe, False caso contrário
        """
        try:
            self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=blob_name
            )
            return True
        except S3Error:
            return False

    def upload_stream(self, file_data, destination_blob_name: str, length: int, content_type: str) -> None:
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=destination_blob_name,
            data=file_data,
            length=length,
            content_type=content_type
        )
