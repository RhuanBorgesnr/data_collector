import os
from datetime import datetime
from typing import Optional
from config import CONFIG

def criar_diretorio_downloads() -> str:
    """Cria o diretório de downloads se não existir."""
    download_path = CONFIG["DOWNLOAD_PATH"]
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path

def gerar_nome_arquivo(cnpj: str, tipo_documento: str, data: Optional[datetime] = None) -> str:
    """Gera um nome único para o arquivo XML."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if data is None else data.strftime("%Y%m%d_%H%M%S")
    return f"{cnpj}_{tipo_documento}_{timestamp}.xml"

def formatar_data_br(data: datetime) -> str:
    """Formata a data para o padrão brasileiro (dd/mm/yyyy)."""
    return data.strftime("%d/%m/%Y") 