"""
rodar_testes.py
===============
Executa os testes automatizados com pytest.

Execute:
    python rodar_testes.py             ← todos os testes
    python rodar_testes.py --cov       ← com relatório de cobertura
    python rodar_testes.py --fast      ← para no primeiro erro (-x)
"""

import sys
import subprocess


def rodar(args: list[str] = []):
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"] + args
    print("Executando:", " ".join(cmd))
    print("=" * 55)
    resultado = subprocess.run(cmd)
    sys.exit(resultado.returncode)


if __name__ == "__main__":
    extras = []
    if "--cov" in sys.argv:
        extras += ["--cov=.", "--cov-report=term-missing"]
    if "--fast" in sys.argv:
        extras += ["-x"]
    rodar(extras)
