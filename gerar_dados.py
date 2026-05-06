"""
gerar_dados.py
==============
Geração de dados sintéticos para treino do modelo de ML.

Execute diretamente:
    python gerar_dados.py

Ou importe a função:
    from gerar_dados import gerar_dataset
"""

import numpy as np
import pandas as pd
from typing import Tuple


# ── Domínio: Fraude ────────────────────────────────────────────────────────────

def gerar_dataset(
    n_samples: int = 1000,
    seed: int = 42,
    proporcao_positivos: float = 0.3,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Gera um dataset sintético de detecção de fraude.

    Features geradas:
    - valor_transacao: transações fraudulentas tendem a ter valores mais altos
    - hora_transacao: fraudes ocorrem mais à noite (0-6h)
    - distancia_ultima_compra: fraudes têm distância maior da última compra
    - tentativas_senha: fraudes têm mais tentativas de senha antes de entrar
    - pais_diferente: flag 0/1 indicando se o país é diferente do usual

    Args:
        n_samples: Número de amostras.
        seed: Semente para reprodutibilidade.
        proporcao_positivos: Proporção da classe positiva (fraude=1).
            Deve estar entre 0.05 e 0.95.

    Returns:
        Tupla (df, X, y) onde df é o DataFrame completo,
        X é a matriz de features e y é o vetor target.

    Raises:
        ValueError: Se proporcao_positivos estiver fora de [0.05, 0.95].

    Example:
        >>> df, X, y = gerar_dataset(n_samples=2000, seed=0, proporcao_positivos=0.2)
        >>> df.shape
        (2000, 6)
    """
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError(
            f"proporcao_positivos deve estar entre 0.05 e 0.95, recebido: {proporcao_positivos}"
        )

    rng = np.random.default_rng(seed)

    fraude = rng.choice(
        [0, 1],
        size=n_samples,
        p=[1 - proporcao_positivos, proporcao_positivos],
    )

    valor_transacao = np.where(
        fraude,
        rng.uniform(500, 10_000, n_samples),
        rng.uniform(10, 800, n_samples),
    ).round(2)

    hora_transacao = np.where(
        fraude,
        rng.integers(0, 6, n_samples),
        rng.integers(7, 23, n_samples),
    )

    distancia_ultima_compra = np.where(
        fraude,
        rng.uniform(100, 5_000, n_samples),
        rng.uniform(0, 50, n_samples),
    ).round(1)

    tentativas_senha = np.where(
        fraude,
        rng.integers(2, 10, n_samples),
        rng.integers(1, 2, n_samples),
    )

    pais_diferente = np.where(
        fraude,
        rng.integers(0, 2, n_samples),
        rng.choice([0, 1], size=n_samples, p=[0.95, 0.05]),
    )

    df = pd.DataFrame({
        "valor_transacao":         valor_transacao,
        "hora_transacao":          hora_transacao,
        "distancia_ultima_compra": distancia_ultima_compra,
        "tentativas_senha":        tentativas_senha,
        "pais_diferente":          pais_diferente,
        "fraude":                  fraude,
    })

    feature_cols = [c for c in df.columns if c != "fraude"]
    X = df[feature_cols].to_numpy()
    y = df["fraude"].to_numpy()

    return df, X, y


if __name__ == "__main__":
    print("=" * 50)
    print("Gerando dataset sintético de fraude...")
    print("=" * 50)

    df, X, y = gerar_dataset(n_samples=2000, seed=42, proporcao_positivos=0.3)

    print(f"\nShape: {df.shape}")
    print(f"\nDistribuição do target:")
    print(df["fraude"].value_counts())
    print(f"\nMédias por classe:")
    print(df.groupby("fraude").mean().round(2).to_string())

    df.to_csv("dados_sinteticos.csv", index=False)
    print("\n✅ Dataset salvo em dados_sinteticos.csv")
