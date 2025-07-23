from storage_service import StorageService
from config import BUCKET_NAME

def exemplo_uso_storage():
    # Inicializa o serviço de armazenamento
    storage = StorageService(BUCKET_NAME)
    
    # Exemplo de upload de arquivo
    caminho_local = "caminho/para/seu/arquivo.txt"
    nome_arquivo_cloud = "pasta/arquivo.txt"
    
    try:
        # Upload de arquivo
        url_arquivo = storage.upload_file(caminho_local, nome_arquivo_cloud)
        print(f"Arquivo enviado com sucesso. URL: {url_arquivo}")
        
        # Listar arquivos
        arquivos = storage.list_files()
        print("Arquivos no bucket:")
        for arquivo in arquivos:
            print(f"- {arquivo}")
        
        # Verificar se arquivo existe
        if storage.file_exists(nome_arquivo_cloud):
            print(f"O arquivo {nome_arquivo_cloud} existe no bucket")
        
        # Download de arquivo
        caminho_download = "caminho/para/download/arquivo.txt"
        storage.download_file(nome_arquivo_cloud, caminho_download)
        print(f"Arquivo baixado para: {caminho_download}")
        
        # Obter URL do arquivo
        url = storage.get_file_url(nome_arquivo_cloud)
        print(f"URL do arquivo: {url}")
        
        # Deletar arquivo
        storage.delete_file(nome_arquivo_cloud)
        print(f"Arquivo {nome_arquivo_cloud} deletado com sucesso")
        
    except Exception as e:
        print(f"Erro ao manipular arquivos: {str(e)}")

if __name__ == "__main__":
    exemplo_uso_storage() 