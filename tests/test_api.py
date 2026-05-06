"""
tests/test_api.py
=================
Testes automatizados da API Bella Tavola.

Execute:
    pytest tests/ -v
    pytest tests/ -v --cov=. --cov-report=term-missing
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ─────────────────────────────────────────────────────────────────────────────
# Root
# ─────────────────────────────────────────────────────────────────────────────

def test_root_retorna_200():
    resp = client.get("/")
    assert resp.status_code == 200


def test_root_contém_restaurante():
    resp = client.get("/")
    data = resp.json()
    assert "restaurante" in data
    assert data["restaurante"] == "Bella Tavola"


# ─────────────────────────────────────────────────────────────────────────────
# Pratos — listagem
# ─────────────────────────────────────────────────────────────────────────────

def test_listar_pratos_retorna_lista():
    resp = client.get("/pratos/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_listar_pratos_tem_campos_obrigatorios():
    resp = client.get("/pratos/")
    pratos = resp.json()
    assert len(pratos) > 0
    for p in pratos:
        assert "id" in p
        assert "nome" in p
        assert "preco" in p
        assert "categoria" in p


def test_filtro_por_categoria():
    resp = client.get("/pratos/?categoria=pizza")
    assert resp.status_code == 200
    for p in resp.json():
        assert p["categoria"] == "pizza"


def test_filtro_por_preco_maximo():
    resp = client.get("/pratos/?preco_maximo=50")
    assert resp.status_code == 200
    for p in resp.json():
        assert p["preco"] <= 50


def test_filtro_combinado():
    resp = client.get("/pratos/?categoria=pizza&preco_maximo=47")
    assert resp.status_code == 200
    for p in resp.json():
        assert p["categoria"] == "pizza"
        assert p["preco"] <= 47


# ─────────────────────────────────────────────────────────────────────────────
# Pratos — busca por ID
# ─────────────────────────────────────────────────────────────────────────────

def test_buscar_prato_existente():
    resp = client.get("/pratos/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1


def test_buscar_prato_inexistente_retorna_404():
    resp = client.get("/pratos/9999")
    assert resp.status_code == 404


# ─────────────────────────────────────────────────────────────────────────────
# Pratos — criação
# ─────────────────────────────────────────────────────────────────────────────

def test_criar_prato_valido():
    payload = {
        "nome": "Arrabbiata",
        "categoria": "massa",
        "preco": 41.0,
        "descricao": "Penne com molho picante",
        "disponivel": True,
    }
    resp = client.post("/pratos/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["nome"] == "Arrabbiata"
    assert data["id"] is not None


def test_criar_prato_preco_negativo_retorna_422():
    payload = {"nome": "Prato Inválido", "categoria": "teste", "preco": -10.0}
    resp = client.post("/pratos/", json=payload)
    assert resp.status_code == 422


def test_criar_prato_nome_vazio_retorna_422():
    payload = {"nome": "", "categoria": "teste", "preco": 30.0}
    resp = client.post("/pratos/", json=payload)
    assert resp.status_code == 422


# ─────────────────────────────────────────────────────────────────────────────
# Pratos — disponibilidade
# ─────────────────────────────────────────────────────────────────────────────

def test_alterar_disponibilidade():
    resp = client.put("/pratos/1/disponibilidade?disponivel=false")
    assert resp.status_code == 200
    assert resp.json()["disponivel"] is False

    # Restaura
    client.put("/pratos/1/disponibilidade?disponivel=true")


def test_prato_indisponivel_nao_aparece_na_listagem():
    client.put("/pratos/2/disponibilidade?disponivel=false")
    resp = client.get("/pratos/")
    ids = [p["id"] for p in resp.json()]
    assert 2 not in ids
    # Restaura
    client.put("/pratos/2/disponibilidade?disponivel=true")


# ─────────────────────────────────────────────────────────────────────────────
# Pedidos
# ─────────────────────────────────────────────────────────────────────────────

def test_criar_pedido_valido():
    payload = {
        "mesa": 3,
        "itens": [{"prato_id": 1, "quantidade": 2}],
    }
    resp = client.post("/pedidos/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["mesa"] == 3
    assert data["total"] > 0
    assert data["status"] == "recebido"


def test_criar_pedido_prato_inexistente_retorna_404():
    payload = {
        "mesa": 1,
        "itens": [{"prato_id": 9999, "quantidade": 1}],
    }
    resp = client.post("/pedidos/", json=payload)
    assert resp.status_code == 404


def test_criar_pedido_sem_itens_retorna_422():
    payload = {"mesa": 1, "itens": []}
    resp = client.post("/pedidos/", json=payload)
    assert resp.status_code == 422


# ─────────────────────────────────────────────────────────────────────────────
# Reservas
# ─────────────────────────────────────────────────────────────────────────────

def _payload_reserva(mesa: int = 5, horas_a_frente: int = 24):
    from datetime import datetime, timedelta, timezone
    dt = datetime.now(timezone.utc) + timedelta(hours=horas_a_frente)
    return {
        "mesa": mesa,
        "nome": "Maria Rossi",
        "pessoas": 4,
        "data_hora": dt.isoformat(),
    }


def test_criar_reserva_valida():
    resp = client.post("/reservas/", json=_payload_reserva(mesa=10))
    assert resp.status_code == 201
    data = resp.json()
    assert data["ativa"] is True


def test_reserva_com_menos_de_1h_retorna_422():
    payload = _payload_reserva(horas_a_frente=0)
    resp = client.post("/reservas/", json=payload)
    assert resp.status_code == 422


def test_reserva_duplicada_retorna_400():
    client.post("/reservas/", json=_payload_reserva(mesa=11))
    resp = client.post("/reservas/", json=_payload_reserva(mesa=11))
    assert resp.status_code == 400


def test_cancelar_reserva():
    resp = client.post("/reservas/", json=_payload_reserva(mesa=12))
    reserva_id = resp.json()["id"]
    del_resp = client.delete(f"/reservas/{reserva_id}")
    assert del_resp.status_code == 200


def test_cancelar_reserva_ja_cancelada_retorna_400():
    resp = client.post("/reservas/", json=_payload_reserva(mesa=13))
    reserva_id = resp.json()["id"]
    client.delete(f"/reservas/{reserva_id}")
    del_resp = client.delete(f"/reservas/{reserva_id}")
    assert del_resp.status_code == 400
