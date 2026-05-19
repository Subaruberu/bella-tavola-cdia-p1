# 🍝 Bella Tavola API & ML Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Este repositório contém o sistema backend do **Bella Tavola**, um restaurante italiano digitalizado. O projeto engloba a construção de uma API RESTful modular, a integração de um modelo de Machine Learning para análise de risco/fraude hospedado no Hugging Face Hub, e um pipeline robusto de Integração Contínua (CI) automatizado.

---

## 🚀 Funcionalidades

### 1. API do Restaurante (FastAPI)
- **Gestão de Cardápio:** CRUD completo para pratos e bebidas com filtros por categoria e preço.
- **Gestão de Pedidos:** Validação de regras de negócio (disponibilidade, cálculo de totais).
- **Reservas Antecipadas:** Sistema de reservas com validação de horário e capacidade de mesas.
- **Validação de Dados:** Uso de modelos Pydantic com `@field_validator` para regras complexas.

### 2. Machine Learning em Produção (MLOps)
- **Geração de Dados Sintéticos:** Pipeline para simular transações e treinar o modelo.
- **Classificação:** Modelo `RandomForestClassifier` treinado e serializado.
- **Model Registry:** Artefato versionado e armazenado no **Hugging Face Hub**.
- **Endpoint de Inferência:** Rota `POST /ml/predict` integrada à API para predições em tempo real com download dinâmico e cache do modelo.
- **Health Check de ML:** Rota `GET /ml/health` que atesta a disponibilidade do artefato.

### 3. Contêinerização com Docker
- **Dockerfile otimizado:** Imagem `python:3.11-slim` com cache de layers configurado (dependências separadas do código).
- **Build reproduzível:** Qualquer máquina com Docker reproduz o ambiente exato de produção.
- **`.dockerignore`:** Build context enxuto — exclui `venv`, `__pycache__`, `.env` e artefatos desnecessários.

### 4. Integração Contínua (CI / GitHub Actions)
- **Qualidade de Código:** Verificações automáticas com `black` e `autoflake`.
- **Testes Automatizados:** Suíte de testes com `pytest` e `TestClient` cobrindo status codes, validações de entrada e regras de negócio.
- **Integração de Recursos Externos:** Testes de sanidade e integração que baixam o modelo de forma segura utilizando **GitHub Secrets** (`HF_TOKEN`).

---

## 📂 Estrutura do Projeto

```text
bella-tavola-cdia-p1-main/
├── .github/workflows/
│   └── ci.yml             # Pipeline de CI (Qualidade, Integração, Relatório)
├── e02/                   # API RESTful do restaurante (FastAPI)
│   ├── models/            # Schemas Pydantic (prato, pedido, reserva, bebida)
│   ├── routers/           # Rotas separadas por domínio
│   ├── tests/             # Suíte de testes (Pytest)
│   ├── config.py          # Variáveis de ambiente (BaseSettings)
│   ├── main.py            # Entry point da API
│   └── requirements.txt
├── e03/                   # Pipeline de ML (treino, serialização, Hugging Face)
│   ├── routers/predict.py # Endpoint POST /ml/predict
│   ├── model_utils.py     # Download e cache do modelo (HF Hub)
│   ├── train.py           # Treinamento do RandomForestClassifier
│   └── requirements.txt
├── e04/                   # GitHub Actions (CI avançado)
└── e05/                   # Contêinerização com Docker
    ├── Dockerfile          # Imagem principal (python:3.11-slim)
    ├── Dockerfile.alpine   # Exercício 9.4 — demonstra falha com Alpine + ML
    ├── .dockerignore       # Exclusões do build context
    ├── main.py             # Entry point (mesma API do e02)
    └── requirements.txt
```
