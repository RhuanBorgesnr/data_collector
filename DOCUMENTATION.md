# Documentação Técnica - Data Extractor

## Visão Geral da Arquitetura

O Data Extractor é uma aplicação Python que combina FastAPI para a interface REST e DrissionPage para automação web. A arquitetura é modular e segue os princípios SOLID.

### Componentes Principais

1. **API Layer (FastAPI)**
   - Endpoints RESTful
   - Validação de dados com Pydantic
   - Documentação automática com Swagger UI
   - Tratamento de erros e respostas padronizadas
   - Middleware de autenticação
   - Rate limiting

2. **Scraping Layer (DrissionPage)**
   - Automação de navegador
   - Interação com elementos web
   - Download de arquivos
   - Gerenciamento de sessão
   - Retry mechanism
   - Timeout handling

3. **Data Layer**
   - Modelos de dados
   - Validação de entrada
   - Transformação de dados
   - Cache management
   - Data persistence

## Configuração do Ambiente

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório | Padrão |
|----------|-----------|-------------|--------|
| AGENCIA_NET_USERNAME | Usuário do portal | Sim | - |
| AGENCIA_NET_PASSWORD | Senha do portal | Sim | - |
| LOG_LEVEL | Nível de log | Não | INFO |
| MAX_RETRIES | Tentativas máximas | Não | 3 |
| TIMEOUT | Timeout em segundos | Não | 30 |

### Configurações do Sistema

O arquivo `config.py` contém as configurações principais:

```python
CONFIG = {
    "BASE_URL": "https://www2.agencianet.fazenda.df.gov.br",
    "LOGIN_URL": "/Inicio/Restrita#/",
    "CONSULTA_URL": "/DEC/#/",
    "WAIT_TIME": 10,  # segundos
    "DOWNLOAD_PATH": "downloads",
    "MAX_CONCURRENT_DOWNLOADS": 5,
    "CLEANUP_INTERVAL": 3600,  # segundos
    "SESSION_TIMEOUT": 1800,  # segundos
}
```

## Detalhes de Implementação

### Autenticação

1. **Processo de Login**
   ```mermaid
   sequenceDiagram
   Client->>+Server: POST /extract
   Server->>+Browser: Inicia sessão
   Browser->>+Portal: Navega para login
   Portal->>Browser: Solicita certificado
   Browser->>Portal: Envia certificado
   Portal->>Browser: Autentica
   Browser->>Server: Sessão estabelecida
   Server->>Client: Job iniciado
   ```

2. **Gerenciamento de Sessão**
   - Cookies persistentes
   - Timeout configurável
   - Recuperação de sessão
   - Session pooling
   - Automatic reconnection

### Extração de Dados

1. **Fluxo de Extração**
   ```mermaid
   graph TD
   A[Início] --> B[Autenticação]
   B --> C[Navegação para Consulta]
   C --> D[Configuração de Filtros]
   D --> E[Download de XML]
   E --> F[Processamento]
   F --> G[Retorno de Resultados]
   ```

2. **Tratamento de Erros**
   - Timeout de conexão
   - Elementos não encontrados
   - Erros de autenticação
   - Falhas no download
   - Network issues
   - Browser crashes

### API Endpoints

#### POST /extract
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "document_type": "NFE",
  "cnpj": "51739827000152",
  "options": {
    "max_retries": 3,
    "timeout": 30
  }
}
```

Resposta:
```json
{
  "status": "success",
  "message": "Extração iniciada",
  "job_id": "uuid",
  "downloads": ["file1.xml", "file2.xml"],
  "estimated_time": "5 minutes"
}
```

#### GET /status/{job_id}
```json
{
  "status": "running",
  "progress": 75,
  "files_downloaded": 3,
  "total_files": 4,
  "current_file": "file4.xml",
  "start_time": "2024-01-01T12:00:00Z",
  "estimated_completion": "2024-01-01T12:05:00Z"
}
```

## Considerações de Segurança

1. **Autenticação**
   - Credenciais em variáveis de ambiente
   - Suporte a certificados digitais
   - Validação de sessão
   - Rate limiting
   - IP whitelisting

2. **Dados**
   - Validação de entrada
   - Sanitização de dados
   - Logs seguros
   - Data encryption
   - Access control

3. **Arquivos**
   - Diretório seguro para downloads
   - Validação de tipos de arquivo
   - Limpeza automática
   - Virus scanning
   - Backup strategy

## Monitoramento e Logs

### Estrutura de Logs
```python
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "job_id": "uuid",
  "message": "Download iniciado",
  "details": {
    "file": "nota_fiscal.xml",
    "size": "1.5MB",
    "url": "https://example.com/file.xml",
    "duration": "2.5s"
  },
  "context": {
    "user": "user123",
    "ip": "192.168.1.1",
    "browser": "Chrome/120.0.0"
  }
}
```

### Métricas
- Tempo de resposta
- Taxa de sucesso
- Volume de dados
- Erros por tipo
- Concurrent users
- Resource usage

## Manutenção

### Rotinas de Limpeza
- Arquivos temporários
- Logs antigos
- Sessões expiradas
- Cache inválido
- Backup rotation

### Atualizações
- Dependências
- Certificados digitais
- Configurações do portal
- Security patches
- Performance optimizations

## Troubleshooting

### Problemas Comuns

1. **Timeout de Autenticação**
   - Verificar conexão
   - Aumentar WAIT_TIME
   - Validar certificado
   - Check firewall
   - Verify DNS

2. **Download Falho**
   - Verificar espaço em disco
   - Validar permissões
   - Checar conexão
   - Check antivirus
   - Verify network speed

3. **Erros de Parsing**
   - Validar formato XML
   - Verificar encoding
   - Atualizar bibliotecas
   - Check file integrity
   - Verify schema

## Contribuição

### Padrões de Código
- PEP 8
- Type hints
- Docstrings
- Testes unitários
- Code coverage
- Linting rules

### Processo de Desenvolvimento
1. Branch por feature
2. Code review
3. CI/CD
4. Versionamento semântico
5. Changelog
6. Release notes 