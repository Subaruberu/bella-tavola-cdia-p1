# e05 — Docker para MLOps: Bella Tavola 🐳

Este diretório contém a API Bella Tavola contêinerizada com Docker, conforme o caderno `e05-p01`.

## Estrutura

```
e05/
├── Dockerfile          # Imagem principal (python:3.11-slim)
├── Dockerfile.alpine   # Exercício 9.4 — demonstra falha com Alpine + scikit-learn
├── .dockerignore       # Arquivos excluídos do build context
├── main.py             # Entry point da API FastAPI
├── requirements.txt    # Dependências Python
├── config.py
├── models/
├── routers/
└── tests/
```

## Como usar

### Build da imagem

```bash
# Na raiz deste diretório (e05/)
docker build -t bella-tavola:v1 .

# Com múltiplas tags (recomendado)
docker build -t bella-tavola:v1 -t bella-tavola:latest .
```

### Rodar o contêiner

```bash
# Foreground (ver logs direto no terminal)
docker run -p 8000:8000 --rm bella-tavola:v1

# Background (detached)
docker run -d -p 8000:8000 --name bella-tavola bella-tavola:v1
```

### Verificar que a API está no ar

```bash
curl http://localhost:8000/
# Esperado: {"restaurante": "Bella Tavola", ...}

curl http://localhost:8000/pratos
# Esperado: lista de pratos em JSON
```

### Gerenciar contêineres

```bash
docker ps                        # contêineres rodando
docker ps -a                     # todos (incluindo parados)
docker logs bella-tavola         # logs do contêiner nomeado
docker stop bella-tavola         # parar
docker rm bella-tavola           # remover
docker images bella-tavola       # listar imagens e tamanhos
```

## Por que essa ordem de instruções no Dockerfile?

```dockerfile
COPY requirements.txt .          # 1º: só o requirements
RUN pip install ...              # 2º: instala dependências (camada cacheada)
COPY . .                         # 3º: copia o código
```

O Docker cacheia camadas. Se `COPY . .` viesse antes do `pip install`,
qualquer alteração em qualquer `.py` invalidaria o cache do `pip install`
— e cada rebuild baixaria todas as dependências novamente (minutos vs. segundos).

## Por que `--host 0.0.0.0` no CMD?

Sem esse flag, o uvicorn escuta em `127.0.0.1` (loopback **interno** ao contêiner).
O mapeamento `-p 8000:8000` roteia para a interface de rede do contêiner —
não para o loopback. Resultado: a porta está mapeada, mas o processo não está escutando lá.
Com `0.0.0.0`, o uvicorn escuta em **todas** as interfaces, inclusive a que conecta ao host.

## Exercício 9.4 — Alpine (Desafio)

```bash
docker build -f Dockerfile.alpine -t bella-tavola:alpine .
```

Esperado: falha durante `pip install` de `scikit-learn` ou `numpy`.
Motivo: Alpine usa `musl libc`; os wheels do PyPI são compilados para `glibc`.
Para projetos de ML, `python:3.11-slim` (Debian) é o equilíbrio correto.
