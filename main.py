from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config import settings
from routers import pratos, pedidos, reservas, predict

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(pratos.router,   prefix="/pratos",   tags=["Pratos"])
app.include_router(pedidos.router,  prefix="/pedidos",  tags=["Pedidos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(predict.router,  prefix="/ml",       tags=["ML"])


# ── Exception handler global ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"erro": "Erro interno do servidor", "detalhe": str(exc)},
    )


# ── Rota raiz ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Marco Rossi",
        "cidade": "São Paulo",
        "especialidade": "Massas artesanais",
    }
