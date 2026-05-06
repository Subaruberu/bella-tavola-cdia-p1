from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

_reservas: List[dict] = []
_next_id = 1


@router.post("/", response_model=ReservaOutput, status_code=201)
async def criar_reserva(reserva: ReservaInput):
    """
    Cria uma reserva antecipada.

    **Regras:**
    - Reserva deve ser feita com pelo menos 1 hora de antecedência
    - Não pode haver duas reservas ativas para a mesma mesa no mesmo dia
    - Número de pessoas limitado por `MAX_PESSOAS_POR_MESA` (config)
    """
    global _next_id
    data_reserva = reserva.data_hora.date()

    conflito = any(
        r["mesa"] == reserva.mesa
        and r["ativa"]
        and datetime.fromisoformat(r["data_hora"]).date() == data_reserva
        for r in _reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {reserva.mesa} já está reservada para {data_reserva}",
        )

    nova = {
        "id": _next_id,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora.isoformat(),
        "ativa": True,
        "criada_em": datetime.now().isoformat(),
    }
    _reservas.append(nova)
    _next_id += 1
    return nova


@router.get("/", response_model=List[ReservaOutput])
async def listar_reservas(
    data: Optional[str] = None,
    apenas_ativas: bool = True,
):
    """
    Lista reservas com filtros opcionais.

    - **data**: formato YYYY-MM-DD
    - **apenas_ativas**: quando True (padrão) omite canceladas
    """
    resultado = _reservas
    if apenas_ativas:
        resultado = [r for r in resultado if r["ativa"]]
    if data:
        resultado = [
            r for r in resultado
            if datetime.fromisoformat(r["data_hora"]).date().isoformat() == data
        ]
    return resultado


@router.get("/mesa/{numero}", response_model=List[ReservaOutput])
async def reservas_por_mesa(numero: int):
    """Retorna todas as reservas de uma mesa específica."""
    return [r for r in _reservas if r["mesa"] == numero]


@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    """Retorna uma reserva específica pelo ID."""
    for r in _reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    """Cancela uma reserva ativa."""
    for r in _reservas:
        if r["id"] == reserva_id:
            if not r["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")
