from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG: Dict[str, Any] = {
    "BASE_URL": "https://www2.agencianet.fazenda.df.gov.br",
    "LOGIN_URL": "/Inicio/Restrita#/",
    "CONSULTA_URL": "/DEC/#/",
    "WAIT_TIME": 10,  # aumentando o tempo de espera para 10 segundos para dar tempo do certificado
    "DOWNLOAD_PATH": "downloads",  # diretório para salvar os arquivos XML
}

# Configurações do ambiente
ENV_CONFIG = {
    "USERNAME": os.getenv("AGENCIA_NET_USERNAME", ""),
    "PASSWORD": os.getenv("AGENCIA_NET_PASSWORD", ""),
} 