"""
setup.py
========
Instala todas as dependências do projeto via pip.

Execute UMA VEZ antes de qualquer outra coisa:
    python setup.py
"""

import subprocess
import sys

DEPENDENCIAS = [
    # API
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.29.0",
    "pydantic>=2.7.0",
    "pydantic-settings>=2.2.0",
    # ML
    "scikit-learn>=1.4.0",
    "joblib>=1.4.0",
    "numpy>=1.26.0",
    "pandas>=2.2.0",
    # Hugging Face
    "huggingface_hub>=0.22.0",
    # Testes
    "pytest>=8.2.0",
    "pytest-cov>=5.0.0",
    "httpx>=0.27.0",
]


def instalar():
    print("=" * 55)
    print("  Instalando dependências do Bella Tavola API")
    print("=" * 55)

    for pkg in DEPENDENCIAS:
        print(f"\n→ {pkg}")
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0:
            print(f"  ❌ Falha: {resultado.stderr.strip()}")
        else:
            print(f"  ✅ OK")

    print("\n" + "=" * 55)
    print("  Instalação concluída!")
    print("\nPróximos passos:")
    print("  1. python env_config.py     ← configura o .env")
    print("  2. uvicorn main:app --reload  ← sobe a API")
    print("  3. python rodar_testes.py   ← roda os testes")
    print("=" * 55)


if __name__ == "__main__":
    instalar()
