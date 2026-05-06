"""
publicar_modelo.py
==================
Publica o model.pkl no Hugging Face Hub com versionamento automático.

Pré-requisitos:
    pip install huggingface_hub
    Configure HF_TOKEN e HF_REPO no .env

Execute:
    python publicar_modelo.py
"""

import sys
from pathlib import Path
from datetime import datetime

MODEL_PATH = Path("model.pkl")


def publicar():
    if not MODEL_PATH.exists():
        print("❌ model.pkl não encontrado. Rode primeiro: python treinar_modelo.py")
        sys.exit(1)

    from config import settings

    if not settings.hf_token:
        print("❌ HF_TOKEN não configurado no .env")
        sys.exit(1)

    if not settings.hf_repo:
        print("❌ HF_REPO não configurado no .env (ex: usuario/bella-tavola-model)")
        sys.exit(1)

    from huggingface_hub import HfApi

    api = HfApi(token=settings.hf_token)

    print(f"📤 Publicando em: {settings.hf_repo}")

    # Cria repositório se não existir
    try:
        api.create_repo(repo_id=settings.hf_repo, exist_ok=True)
        print(f"   Repositório OK: https://huggingface.co/{settings.hf_repo}")
    except Exception as exc:
        print(f"⚠️  Aviso ao criar repositório: {exc}")

    # Faz upload do modelo
    api.upload_file(
        path_or_fileobj=str(MODEL_PATH),
        path_in_repo="model.pkl",
        repo_id=settings.hf_repo,
        token=settings.hf_token,
        commit_message=f"Atualiza model.pkl — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )
    print("✅ model.pkl publicado com sucesso!")

    # Gera model card básico
    readme_content = f"""---
language: pt
tags:
  - sklearn
  - fraud-detection
  - fastapi
---

# Bella Tavola — Modelo de Detecção de Fraude

Modelo treinado com dados sintéticos gerados por `gerar_dados.py`.

## Features (nessa ordem)

| # | Feature | Tipo |
|---|---------|------|
| 0 | valor_transacao | float |
| 1 | hora_transacao | int |
| 2 | distancia_ultima_compra | float |
| 3 | tentativas_senha | int |
| 4 | pais_diferente | int (0/1) |

## Como usar via API

```bash
curl -X POST http://localhost:8000/ml/predict \\
  -H "Content-Type: application/json" \\
  -d '{{"features": [1500.0, 2, 300.5, 4, 1]}}'
```

## Última publicação

{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    api.upload_file(
        path_or_fileobj=readme_content.encode(),
        path_in_repo="README.md",
        repo_id=settings.hf_repo,
        token=settings.hf_token,
        commit_message="Atualiza README / model card",
    )
    print("✅ README (model card) atualizado!")


if __name__ == "__main__":
    publicar()
