# e05 — Docker para MLOps: Bella Tavola 🐳

Contêinerização completa da API Bella Tavola com Docker e Docker Compose.

## Estrutura

```
e05/
├── Dockerfile              # Multi-stage build + usuário não-root (python:3.11-slim)
├── Dockerfile.alpine       # Exercício 9.4 — demonstra falha com Alpine + scikit-learn
├── .dockerignore           # Exclui do build context: .env, tests/, *.pkl, __pycache__ etc.
├── docker-compose.yml      # Orquestra API + PostgreSQL + Nginx com healthcheck
├── nginx.conf              # Proxy reverso: porta 80 → uvicorn porta 8000
├── main.py                 # Entry point da API FastAPI
├── requirements.txt        # Dependências Python
├── config.py
├── models/
├── routers/
└── tests/
```

## Como usar

### Subir o stack completo (API + PostgreSQL + Nginx)

```bash
# Na raiz deste diretório (e05/)
# Certifique-se de que o .env existe com HF_TOKEN=hf_...

docker compose up           # foreground — logs visíveis
docker compose up -d        # background (detached)
```

A API responde via Nginx em **http://localhost** (porta 80).

```bash
curl http://localhost/
curl http://localhost/pratos

curl -X POST http://localhost/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"valor_transacao": 150.0, "hora_transacao": 14,
       "distancia_ultima_compra": 5.0, "tentativas_senha": 1,
       "pais_diferente": 0}'
```

### Comandos Compose essenciais

```bash
docker compose ps                  # status dos serviços
docker compose logs -f api         # logs da API em tempo real
docker compose logs db             # logs do PostgreSQL
docker compose exec api bash       # shell dentro do contêiner da API
docker compose restart api         # reinicia só a API

docker compose down                # para e remove contêineres (preserva volumes)
docker compose down -v             # para, remove contêineres E volumes (dados perdidos)
```

### Build manual (sem Compose)

```bash
docker build -t bella-tavola:v3 .

# Rodar com token e volume
docker run -p 8000:8000 --rm \
  --env-file .env \
  -v bella-dados:/app/data \
  bella-tavola:v3
```

### Verificar segurança

```bash
# Confirmar que o processo roda como usuário não-root
docker run --rm bella-tavola:v3 whoami
# Esperado: appuser

# Confirmar que .env não está na imagem
docker run --rm bella-tavola:v3 find /app -name '.env'
# Esperado: nenhuma saída
```

## Arquitetura dos serviços

```
Usuário
  │
  ▼ porta 80
┌─────────┐
│  Nginx  │  proxy reverso
└────┬────┘
     │ rede interna (api:8000)
     ▼
┌─────────┐        ┌──────────────┐
│   API   │──────► │  PostgreSQL  │
│ uvicorn │        │   porta 5432 │
└─────────┘        └──────────────┘
```

- **Nginx** é o único serviço exposto ao host (porta 80)
- **API** fica na rede interna do Compose — não exposta diretamente
- **PostgreSQL** também na rede interna, acessado pela API via hostname `db`
- Serviços se comunicam por **nome do serviço** (não `localhost`)

## Decisões de design do Dockerfile

### Multi-stage build
O estágio `builder` instala as dependências (requer compiladores). O estágio `final` copia apenas os pacotes instalados — sem compiladores, sem cache, sem resíduos de build. Redução típica de 30–40% no tamanho da imagem.

### Usuário não-root
A API roda como `appuser` (sem privilégios). Se um atacante explorar uma vulnerabilidade, não terá acesso root dentro do contêiner.

### Ordem das instruções (cache de layers)
```
COPY requirements.txt   →  pip install  →  COPY . .
```
Mudanças no código não reexecutam o `pip install` (que pode levar minutos). Só muda quando o `requirements.txt` muda.

## Por que `localhost` não funciona entre serviços

Dentro de um contêiner, `localhost` é o próprio contêiner — não o banco, não o Nginx. No Compose, use o **nome do serviço** como hostname:

```
# ERRADO
DATABASE_URL: postgresql://bella:secreta@localhost:5432/bellatavolada

# CORRETO
DATABASE_URL: postgresql://bella:secreta@db:5432/bellatavolada
#                                          ↑ nome do serviço no compose.yml
```

## Exercício 9.4 — Alpine (Desafio)

```bash
docker build -f Dockerfile.alpine -t bella-tavola:alpine .
```

Esperado: falha no `pip install` de `scikit-learn` ou `numpy`. Alpine usa `musl libc`; os wheels do PyPI são compilados para `glibc`. Use `python:3.11-slim` para projetos de ML.
