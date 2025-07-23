from minio import Minio
from minio.error import S3Error
from typing import Optional, List
import os
from .config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_BUCKET_NAME

class StorageService:
    def __init__(self):
        self.client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        self.bucket_name = MINIO_BUCKET_NAME
        
        if not self.client.bucket_exists(MINIO_BUCKET_NAME):
            self.client.make_bucket(MINIO_BUCKET_NAME)
    
    def upload_file(self, source_file_path: str, destination_blob_name: str) -> str:
        self.client.fput_object(
            bucket_name=self.bucket_name,
            object_name=destination_blob_name,
            file_path=source_file_path
        )
        
        return self.get_file_url(destination_blob_name)
    
    def download_file(self, source_blob_name: str, destination_file_path: str) -> None:
        self.client.fget_object(
            bucket_name=self.bucket_name,
            object_name=source_blob_name,
            file_path=destination_file_path
        )
    
    def get_file_url(self, blob_name: str) -> str:
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=blob_name
            )
            return url
        except S3Error:
            return ""
    
    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        objects = self.client.list_objects(
            bucket_name=self.bucket_name,
            prefix=prefix or ""
        )
        return [obj.object_name for obj in objects]
    
    def delete_file(self, blob_name: str) -> None:
        self.client.remove_object(
            bucket_name=self.bucket_name,
            object_name=blob_name
        )
    
    def file_exists(self, blob_name: str) -> bool:
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
