from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.pedido import PedidoInput, PedidoOutput

# Importamos a lista de pratos do router de pratos (em produção, use um DB)
from routers.pratos import _pratos

router = APIRouter()

_pedidos: List[dict] = []
_next_id = 1


@router.post("/", response_model=PedidoOutput, status_code=201)
async def criar_pedido(pedido: PedidoInput):
    """
    Cria um novo pedido.

    Valida se todos os pratos informados existem e estão disponíveis.
    Calcula o total automaticamente.
    """
    global _next_id
    total = 0.0
    for item in pedido.itens:
        prato = next((p for p in _pratos if p["id"] == item.prato_id), None)
        if prato is None:
            raise HTTPException(
                status_code=404,
                detail=f"Prato ID {item.prato_id} não encontrado",
            )
        if not prato["disponivel"]:
            raise HTTPException(
                status_code=400,
                detail=f"Prato '{prato['nome']}' está indisponível no momento",
            )
        total += prato["preco"] * item.quantidade

    novo = {
        "id": _next_id,
        "mesa": pedido.mesa,
        "itens": [i.model_dump() for i in pedido.itens],
        "total": round(total, 2),
        "status": "recebido",
        "criado_em": datetime.now().isoformat(),
    }
    _pedidos.append(novo)
    _next_id += 1
    return novo


@router.get("/", response_model=List[PedidoOutput])
async def listar_pedidos():
    """Lista todos os pedidos."""
    return _pedidos


@router.get("/{pedido_id}", response_model=PedidoOutput)
async def buscar_pedido(pedido_id: int):
    """Retorna um pedido específico pelo ID."""
    for p in _pedidos:
        if p["id"] == pedido_id:
            return p
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
