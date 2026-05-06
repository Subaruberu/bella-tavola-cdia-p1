from fastapi import APIRouter, HTTPException
from typing import Optional, List
from models.prato import PratoInput, PratoOutput

router = APIRouter()

# ── Dados em memória (substitua por banco em produção) ────────────────────────
_pratos: List[dict] = [
    {"id": 1, "nome": "Margherita",       "categoria": "pizza",     "preco": 45.0, "descricao": "Molho de tomate, muçarela e manjericão", "disponivel": True},
    {"id": 2, "nome": "Carbonara",        "categoria": "massa",     "preco": 52.0, "descricao": "Espaguete, guanciale, ovo e pecorino",    "disponivel": True},
    {"id": 3, "nome": "Lasanha Bolonhesa","categoria": "massa",     "preco": 58.0, "descricao": "Ragù clássico com béchamel",              "disponivel": True},
    {"id": 4, "nome": "Tiramisù",         "categoria": "sobremesa", "preco": 28.0, "descricao": "Mascarpone, café e biscoito savoiardi",   "disponivel": True},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza",     "preco": 49.0, "descricao": "Quatro seções com coberturas distintas",  "disponivel": True},
    {"id": 6, "nome": "Panna Cotta",      "categoria": "sobremesa", "preco": 24.0, "descricao": "Creme com calda de frutas vermelhas",     "disponivel": True},
]
_next_id = 7


# ── Rotas ─────────────────────────────────────────────────────────────────────
@router.get("/", response_model=List[PratoOutput])
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = True,
):
    """
    Lista todos os pratos do cardápio.

    - **categoria**: filtra por categoria (ex: pizza, massa, sobremesa)
    - **preco_maximo**: retorna somente pratos até este valor em R$
    - **apenas_disponiveis**: quando True (padrão) oculta pratos indisponíveis
    """
    resultado = _pratos
    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    return resultado


@router.get("/{prato_id}", response_model=PratoOutput)
async def buscar_prato(prato_id: int):
    """Retorna os detalhes de um prato específico pelo ID."""
    for prato in _pratos:
        if prato["id"] == prato_id:
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    """Cadastra um novo prato no cardápio."""
    global _next_id
    novo = {"id": _next_id, **prato.model_dump()}
    _pratos.append(novo)
    _next_id += 1
    return novo


@router.put("/{prato_id}/disponibilidade", response_model=PratoOutput)
async def alterar_disponibilidade(prato_id: int, disponivel: bool):
    """Ativa ou desativa a disponibilidade de um prato."""
    for prato in _pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = disponivel
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")
