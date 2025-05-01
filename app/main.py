from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional

from .models import ScrapingRequest, ScrapingResponse
from .scraping import Scraper

app = FastAPI(
    title="Data Extractor API",
    description="API para extração de documentos fiscais",
    version="1.0.0"
)

@app.post("/iniciar_scraping", response_model=ScrapingResponse)
async def iniciar_scraping(request: ScrapingRequest) -> ScrapingResponse:
    """
    Inicia o processo de scraping para os documentos fiscais.
    
    Args:
        request: Dados da requisição contendo CNPJ, tipo de documento e período
        
    Returns:
        ScrapingResponse: Resposta com o status da operação
    """
    try:
        scraper = Scraper()
        
        # Realizar login
        if not scraper.login():
            raise HTTPException(status_code=401, detail="Falha no login")
        
        # Preencher campos e iniciar busca
        if not scraper.preencher_campos(
            cnpj=request.cnpj,
            tipo_documento=request.tipo_documento,
            data_inicio=request.data_inicio,
            data_fim=request.data_fim
        ):
            raise HTTPException(status_code=400, detail="Falha ao preencher campos")
        
        # Verificar e baixar resultados
        arquivos_baixados = scraper.verificar_resultados()
        
        return ScrapingResponse(
            message="Scraping concluído com sucesso",
            status="success",
            arquivos_baixados=arquivos_baixados
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API."""
    return {"status": "healthy"} 