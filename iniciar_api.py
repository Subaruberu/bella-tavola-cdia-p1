"""
iniciar_api.py
==============
Inicia o servidor uvicorn da API Bella Tavola.

Execute:
    python iniciar_api.py              ← modo padrão (--reload)
    python iniciar_api.py --prod       ← modo produção (sem reload)
    python iniciar_api.py --port 9000  ← porta customizada
"""

import sys
import uvicorn

HOST = "0.0.0.0"
PORT = 8000
RELOAD = True

# Lê argumentos simples sem argparse para manter zero dependências extras
args = sys.argv[1:]
if "--prod" in args:
    RELOAD = False
if "--port" in args:
    idx = args.index("--port")
    PORT = int(args[idx + 1])

if __name__ == "__main__":
    print(f"🍝 Bella Tavola API")
    print(f"   Host   : http://{HOST}:{PORT}")
    print(f"   Swagger: http://localhost:{PORT}/docs")
    print(f"   ReDoc  : http://localhost:{PORT}/redoc")
    print(f"   Reload : {RELOAD}")
    print()

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level="info",
    )
