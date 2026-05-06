from pydantic import BaseModel, Field
from typing import Optional


class PratoInput(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    categoria: str = Field(min_length=2, max_length=50)
    preco: float = Field(gt=0, description="Preço em R$ (deve ser positivo)")
    descricao: Optional[str] = Field(default=None, max_length=300)
    disponivel: bool = True


class PratoOutput(PratoInput):
    id: int
