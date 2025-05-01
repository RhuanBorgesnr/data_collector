from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class ScrapingRequest(BaseModel):
    """Modelo para requisição de scraping."""
    cnpj: str = Field(..., min_length=14, max_length=14, description="CNPJ da empresa")
    tipo_documento: Literal["NFE", "NFSE"] = Field(..., description="Tipo do documento fiscal")
    data_inicio: date = Field(..., description="Data inicial da consulta")
    data_fim: date = Field(..., description="Data final da consulta")

class ScrapingResponse(BaseModel):
    """Modelo para resposta do scraping."""
    message: str = Field(..., description="Mensagem de retorno da operação")
    status: str = Field(..., description="Status da operação")
    arquivos_baixados: int = Field(default=0, description="Quantidade de arquivos baixados") 