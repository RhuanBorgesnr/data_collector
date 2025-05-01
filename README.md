# Data Extractor - Agência Net DF

Este projeto é um extrator de dados automatizado para o portal da Agência Net DF, desenvolvido em Python utilizando FastAPI e DrissionPage.

## 🚀 Funcionalidades

- Autenticação automática no portal da Agência Net DF
- Extração de dados de documentos fiscais
- Download automático de arquivos XML
- API REST para integração com outros sistemas
- Suporte a certificados digitais
- Monitoramento de status em tempo real
- Gerenciamento de sessões persistentes

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Certificado digital A1 ou A3 (opcional)
- 1GB de espaço livre em disco
- Conexão estável com a internet

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/data_extractor.git
cd data_extractor
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
AGENCIA_NET_USERNAME=seu_usuario
AGENCIA_NET_PASSWORD=sua_senha
```

## 🛠️ Estrutura do Projeto

```
data_extractor/
├── app/
│   ├── __init__.py
│   ├── main.py          # API FastAPI
│   ├── models.py        # Modelos de dados
│   ├── scraping.py      # Lógica de scraping
│   └── utils.py         # Funções utilitárias
├── downloads/           # Diretório para arquivos baixados
├── config.py           # Configurações do projeto
├── requirements.txt    # Dependências
├── README.md          # Documentação principal
└── DOCUMENTATION.md   # Documentação técnica detalhada
```

## 🚀 Como Usar

1. Inicie o servidor FastAPI:
```bash
uvicorn app.main:app --reload
```

2. Acesse a documentação da API em:
```
http://localhost:8000/docs
```

## 📚 Documentação da API

### Endpoints Disponíveis

- `POST /extract`: Inicia o processo de extração de dados
- `GET /status/{job_id}`: Verifica o status de um job específico
- `GET /downloads`: Lista os arquivos baixados
- `GET /health`: Verifica a saúde do serviço

### Exemplo de Uso

```python
import requests

# Iniciar extração
response = requests.post(
    "http://localhost:8000/extract",
    json={
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "document_type": "NFE",
        "cnpj": "51739827000152"
    }
)

# Verificar status
job_id = response.json()["job_id"]
status = requests.get(f"http://localhost:8000/status/{job_id}")
```

## 🔒 Segurança

- As credenciais são armazenadas em variáveis de ambiente
- Suporte a certificados digitais para autenticação
- Validação de dados de entrada
- Tratamento de erros e exceções
- Logs seguros e não sensíveis
- Limpeza automática de arquivos temporários

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte, envie um email para seu-email@exemplo.com ou abra uma issue no GitHub.

Para documentação técnica detalhada, consulte o arquivo [DOCUMENTATION.md](DOCUMENTATION.md). 