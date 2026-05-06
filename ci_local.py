"""
ci_local.py
===========
Simula o pipeline de CI (GitHub Actions) rodando localmente.

Equivalente ao .github/workflows/ci.yml — mesmas etapas,
mesma lógica, 100% Python.

Execute:
    python ci_local.py

Saída:
    ✅ / ❌ por etapa, com tempo de execução e resumo final.
"""

import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# ── Utilitários ───────────────────────────────────────────────────────────────

def _titulo(texto: str):
    print(f"\n{'─' * 55}")
    print(f"  {texto}")
    print(f"{'─' * 55}")


def _rodar(cmd: list[str], env_extra: dict | None = None) -> tuple[int, str]:
    import os
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    saida = proc.stdout + proc.stderr
    return proc.returncode, saida


def _ok(etapa: str, duracao: float):
    print(f"✅  {etapa}  ({duracao:.1f}s)")


def _falhou(etapa: str, saida: str, duracao: float):
    print(f"❌  {etapa}  ({duracao:.1f}s)")
    print("\nSaída do comando:")
    print(saida[-2000:])   # últimas 2000 chars para não poluir demais


# ── Etapas do pipeline ────────────────────────────────────────────────────────

def etapa_dependencias() -> bool:
    _titulo("ETAPA 1 — Verificar dependências instaladas")
    pacotes = [
        "fastapi", "uvicorn", "pydantic", "pydantic_settings",
        "sklearn", "joblib", "numpy", "pandas",
        "huggingface_hub", "pytest", "httpx",
    ]
    faltando = []
    for pkg in pacotes:
        t0 = time.time()
        codigo, _ = _rodar([sys.executable, "-c", f"import {pkg}"])
        if codigo != 0:
            faltando.append(pkg)

    if faltando:
        print(f"❌ Pacotes ausentes: {', '.join(faltando)}")
        print("   Execute: python setup.py")
        return False

    _ok("Todas as dependências encontradas", 0)
    return True


def etapa_lint() -> bool:
    _titulo("ETAPA 2 — Lint (verificação de estilo)")
    t0 = time.time()

    # Tenta usar ruff; se não tiver, usa pyflakes como fallback
    codigo, saida = _rodar([sys.executable, "-m", "ruff", "check", ".",
                            "--select", "E,F,W", "--ignore", "E501"])
    duracao = time.time() - t0

    if codigo == 0:
        _ok("Lint passou (ruff)", duracao)
        return True

    # ruff não instalado → fallback para pyflakes
    codigo2, saida2 = _rodar([sys.executable, "-m", "pyflakes", "."])
    duracao = time.time() - t0
    if codigo2 == 0:
        _ok("Lint passou (pyflakes)", duracao)
        return True

    # Lint com avisos mas não bloqueia (continue-on-error: true no CI)
    print(f"⚠️   Lint encontrou avisos — não bloqueia ({duracao:.1f}s)")
    print(saida[-1000:])
    return True   # mesmo comportamento do ci.yml (continue-on-error)


def etapa_testes() -> bool:
    _titulo("ETAPA 3 — Testes automatizados (pytest)")
    t0 = time.time()
    codigo, saida = _rodar([
        sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
    ])
    duracao = time.time() - t0

    if codigo == 0:
        _ok("Todos os testes passaram", duracao)
        return True
    else:
        _falhou("Testes falharam", saida, duracao)
        return False


def etapa_smoke_test() -> bool:
    _titulo("ETAPA 4 — Smoke test (API sobe e responde?)")

    # Sobe a API em background
    import os
    import signal

    print("  Iniciando uvicorn em background...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "127.0.0.1", "--port", "18000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Aguarda a API subir (máx 10s)
    t0 = time.time()
    subiu = False
    for _ in range(20):
        time.sleep(0.5)
        try:
            urllib.request.urlopen("http://127.0.0.1:18000/", timeout=2)
            subiu = True
            break
        except Exception:
            pass

    if not subiu:
        proc.terminate()
        _falhou("API não subiu dentro do prazo", "", time.time() - t0)
        return False

    # Testa rotas
    rotas_ok = True
    for rota in ["/", "/pratos/"]:
        try:
            resp = urllib.request.urlopen(
                f"http://127.0.0.1:18000{rota}", timeout=5
            )
            status = resp.getcode()
            if status == 200:
                print(f"  ✅  GET {rota} → {status}")
            else:
                print(f"  ❌  GET {rota} → {status}")
                rotas_ok = False
        except urllib.error.HTTPError as e:
            print(f"  ❌  GET {rota} → {e.code}")
            rotas_ok = False
        except Exception as e:
            print(f"  ❌  GET {rota} → erro: {e}")
            rotas_ok = False

    proc.terminate()
    duracao = time.time() - t0

    if rotas_ok:
        _ok("Smoke test passou", duracao)
        return True
    else:
        _falhou("Smoke test falhou", "", duracao)
        return False


# ── Runner principal ──────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("  CI LOCAL — Bella Tavola API")
    print("  Simulação do pipeline GitHub Actions")
    print("=" * 55)

    etapas = [
        ("Dependências",  etapa_dependencias),
        ("Lint",          etapa_lint),
        ("Testes",        etapa_testes),
        ("Smoke test",    etapa_smoke_test),
    ]

    resultados = {}
    for nome, fn in etapas:
        ok = fn()
        resultados[nome] = ok
        if not ok and nome in ("Dependências", "Testes"):
            print(f"\n⛔ Pipeline interrompido em: {nome}")
            break

    # Resumo final
    print("\n" + "=" * 55)
    print("  RESUMO DO PIPELINE")
    print("=" * 55)
    tudo_ok = True
    for nome, ok in resultados.items():
        icone = "✅" if ok else "❌"
        print(f"  {icone}  {nome}")
        if not ok:
            tudo_ok = False

    print()
    if tudo_ok:
        print("🎉 Pipeline passou! Pronto para o push/PR.")
    else:
        print("💥 Pipeline falhou. Corrija os erros antes de fazer push.")

    sys.exit(0 if tudo_ok else 1)


if __name__ == "__main__":
    main()
