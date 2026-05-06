from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()


class PredictInput(BaseModel):
    features: List[float] = Field(
        min_length=1,
        description="Lista de valores das features na ordem esperada pelo modelo",
        examples=[[0.5, 1.2, -0.3, 2.1, 0.8]],
    )


class PredictOutput(BaseModel):
    classe: int
    probabilidade: float


@router.post("/predict", response_model=PredictOutput)
async def predict_endpoint(payload: PredictInput):
    """
    Executa uma predição usando o modelo treinado.

    O modelo é carregado do Hugging Face Hub (ou do cache local)
    na primeira requisição.
    """
    try:
        from model_utils import predict
        resultado = predict(payload.features)
        return resultado
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Erro na predição: {exc}",
        )


@router.post("/predict/reload")
async def reload_model():
    """Força o re-download do modelo do Hugging Face Hub."""
    try:
        from model_utils import load_model
        load_model(force_download=True)
        return {"mensagem": "Modelo recarregado com sucesso"}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
