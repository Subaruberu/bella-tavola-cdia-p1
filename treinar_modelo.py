"""
treinar_modelo.py
=================
Treina, avalia e serializa o modelo de ML.

Execute:
    python treinar_modelo.py

Resultado:
    model.pkl  — artefato pronto para uso na API e para upload no Hugging Face Hub
"""

import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score

from gerar_dados import gerar_dataset

# ── Configurações ─────────────────────────────────────────────────────────────
SEED = 42
N_SAMPLES = 5_000
TEST_SIZE = 0.2
MODEL_PATH = Path("model.pkl")

# ── Pipeline ──────────────────────────────────────────────────────────────────

def treinar():
    print("1/4 – Gerando dados sintéticos...")
    df, X, y = gerar_dataset(n_samples=N_SAMPLES, seed=SEED, proporcao_positivos=0.3)

    print(f"     {len(df)} amostras | {(y == 1).sum()} positivos ({(y == 1).mean():.1%})")

    print("2/4 – Dividindo treino/teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y
    )

    print("3/4 – Treinando RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        class_weight="balanced",
        random_state=SEED,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # Validação cruzada
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    print(f"     CV ROC-AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    print("4/4 – Avaliando no conjunto de teste...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print(f"\n{'='*50}")
    print("Classification Report (teste):")
    print(classification_report(y_test, y_pred, target_names=["Legítimo", "Fraude"]))
    print(f"ROC-AUC (teste): {roc_auc_score(y_test, y_prob):.4f}")
    print(f"{'='*50}\n")

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Modelo salvo em: {MODEL_PATH}")

    # Ordem das features (importante para o endpoint /predict)
    feature_names = ["valor_transacao", "hora_transacao", "distancia_ultima_compra",
                     "tentativas_senha", "pais_diferente"]
    print(f"\n📋 Ordem das features esperada pelo modelo:")
    for i, name in enumerate(feature_names):
        print(f"   [{i}] {name}")

    return model


if __name__ == "__main__":
    treinar()
