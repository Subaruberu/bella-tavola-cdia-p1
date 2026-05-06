from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime


class ItemPedido(BaseModel):
    prato_id: int
    quantidade: int = Field(ge=1)


class PedidoInput(BaseModel):
    mesa: int = Field(ge=1)
    itens: List[ItemPedido] = Field(min_length=1)

    @field_validator("itens")
    @classmethod
    def itens_nao_vazios(cls, v):
        if not v:
            raise ValueError("O pedido deve ter pelo menos um item")
        return v


class PedidoOutput(BaseModel):
    id: int
    mesa: int
    itens: List[ItemPedido]
    total: float
    status: str
    criado_em: str
