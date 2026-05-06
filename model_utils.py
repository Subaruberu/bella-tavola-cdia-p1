"""
model_utils.py
==============
Utilitários para carregar e usar o modelo de ML.

O modelo é baixado do Hugging Face Hub na primeira chamada
e armazenado localmente em `model.pkl` para evitar downloads repetidos.
"""

import os
import joblib
import logging
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)

MODEL_PATH = Path("model.pkl")
_model = None  # cache em memória


def load_model(force_download: bool = False):
    """
    Carrega o modelo de ML.

    Estratégia:
    1. Se já está em memória, retorna direto.
    2. Se `model.pkl` existe localmente e não forçamos download, carrega do disco.
    3. Caso contrário, baixa do Hugging Face Hub.

    Args:
        force_download: Ignora cache local e baixa novamente do Hub.

    Returns:
        Modelo scikit-learn carregado.

    Raises:
        RuntimeError: Se o token HF não estiver configurado e o modelo não existir localmente.
    """
    global _model

    if _model is not None and not force_download:
        return _model

    if MODEL_PATH.exists() and not force_download:
        logger.info("Carregando modelo do disco local: %s", MODEL_PATH)
        _model = joblib.load(MODEL_PATH)
        return _model

    # Download do Hugging Face Hub
    if not settings.hf_token or not settings.hf_repo:
        raise RuntimeError(
            "HF_TOKEN e HF_REPO devem estar configurados no .env para baixar o modelo."
        )

    logger.info("Baixando modelo do Hugging Face Hub: %s", settings.hf_repo)
    try:
        from huggingface_hub import hf_hub_download

        local_path = hf_hub_download(
            repo_id=settings.hf_repo,
            filename="model.pkl",
            token=settings.hf_token,
        )
        _model = joblib.load(local_path)
        # Salva localmente para cache
        joblib.dump(_model, MODEL_PATH)
        logger.info("Modelo salvo em cache: %s", MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(f"Erro ao baixar modelo do Hub: {exc}") from exc

    return _model


def predict(features: list) -> dict:
    """
    Executa uma predição.

    Args:
        features: Lista de valores na ordem correta das features.

    Returns:
        Dicionário com `classe` (int) e `probabilidade` (float).
    """
    model = load_model()
    import numpy as np

    X = np.array(features).reshape(1, -1)
    classe = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][classe])
    return {"classe": classe, "probabilidade": round(prob, 4)}
