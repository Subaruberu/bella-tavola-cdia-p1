# Bella Tavola API 🍝

API RESTful para o restaurante Bella Tavola, com integração de modelo de ML para detecção de fraude.

Construída com **FastAPI**, **scikit-learn** e **Hugging Face Hub**. Pipeline de CI com **GitHub Actions**.

---

## Estrutura do projeto

```
bella_tavola/
├── main.py                    # Ponto de entrada da API
├── config.py                  # Configurações via pydantic-settings
├── model_utils.py             # Carregamento do modelo (HF Hub ou local)
├── gerar_dados.py             # Geração de dados sintéticos
├── treinar_modelo.py          # Treinamento e serialização do modelo
├── publicar_modelo.py         # Upload do modelo para o Hugging Face Hub
├── requirements.txt
├── .env.example               # Modelo do arquivo de configuração local
├── .gitignore
│
├── models/                    # Modelos Pydantic
│   ├── prato.py
│   ├── pedido.py
│   └── reserva.py
│
├── routers/                   # Rotas organizadas por domínio
│   ├── pratos.py
│   ├── pedidos.py
│   ├── reservas.py
│   └── predict.py
│
├── tests/
│   └── test_api.py            # Testes automatizados com pytest
│
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de CI com GitHub Actions
│
└── .vscode/
    ├── settings.json          # Configurações do editor
    └── launch.json            # Atalhos de run/debug
```

---

## Configuração do ambiente (VSCode)

### 1. Clonar e abrir no VSCode

```bash
git clone <url-do-seu-repositorio>
cd bella_tavola
code .
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha:

```bash
cp .env.example .env
```

Edite `.env` com seu token do Hugging Face e o nome do repositório:

```
HF_TOKEN=hf_SEU_TOKEN_AQUI
HF_REPO=seu-usuario/bella-tavola-model
```

> Obtenha seu token em: https://huggingface.co/settings/tokens  
> Crie um token com permissão de **escrita**.

---

## Rodando a API

### Via terminal

```bash
uvicorn main:app --reload
```

A API estará disponível em:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Via VSCode (Run & Debug)

Pressione `F5` e escolha **🚀 Rodar API (uvicorn --reload)**.

---

## Rodando os testes

```bash
# Todos os testes
pytest tests/ -v

# Com relatório de cobertura
pytest tests/ -v --cov=. --cov-report=term-missing

# Via VSCode: F5 → "🧪 Pytest — todos os testes"
```

---

## Pipeline de ML

### 1. Gerar dados sintéticos

```bash
python gerar_dados.py
# Gera: dados_sinteticos.csv
```

### 2. Treinar o modelo

```bash
python treinar_modelo.py
# Gera: model.pkl
```

### 3. Publicar no Hugging Face Hub

```bash
python publicar_modelo.py
```

### 4. Testar o endpoint de predição

```bash
curl -X POST http://localhost:8000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1500.0, 2, 300.5, 4, 1]}'
```

**Ordem das features:**

| # | Feature | Descrição |
|---|---------|-----------|
| 0 | valor_transacao | Valor em R$ |
| 1 | hora_transacao | Hora do dia (0-23) |
| 2 | distancia_ultima_compra | Distância em km |
| 3 | tentativas_senha | Número de tentativas |
| 4 | pais_diferente | 0 = não, 1 = sim |

---

## Rotas disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Informações do restaurante |
| GET | `/pratos/` | Lista pratos (filtros: categoria, preco_maximo) |
| GET | `/pratos/{id}` | Detalha um prato |
| POST | `/pratos/` | Cadastra um prato |
| PUT | `/pratos/{id}/disponibilidade` | Altera disponibilidade |
| POST | `/pedidos/` | Cria um pedido |
| GET | `/pedidos/` | Lista pedidos |
| GET | `/pedidos/{id}` | Detalha um pedido |
| POST | `/reservas/` | Cria reserva antecipada |
| GET | `/reservas/` | Lista reservas |
| GET | `/reservas/{id}` | Detalha uma reserva |
| GET | `/reservas/mesa/{numero}` | Reservas por mesa |
| DELETE | `/reservas/{id}` | Cancela uma reserva |
| POST | `/ml/predict` | Executa predição |
| POST | `/ml/predict/reload` | Recarrega modelo do Hub |

---

## GitHub Actions (CI)

O arquivo `.github/workflows/ci.yml` configura um pipeline que roda automaticamente a cada **push** e **pull request** no branch `main`.

**O pipeline:**
1. Instala as dependências
2. Roda lint (ruff)
3. Executa todos os testes (pytest)
4. Faz um smoke test subindo a API e verificando a rota raiz

**Configure os Secrets no GitHub** (Settings → Secrets → Actions):
- `HF_TOKEN` — seu token do Hugging Face
- `HF_REPO` — nome do repositório (ex: `usuario/bella-tavola-model`)
