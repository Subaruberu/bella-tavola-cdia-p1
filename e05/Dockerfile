# ── Estágio 1: builder ────────────────────────────────────────────────────────
# Tem tudo que é necessário para INSTALAR as dependências.
# Compiladores, headers e cache do pip ficam aqui — e são descartados depois.
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

# --prefix=/install: instala os pacotes em /install em vez de /usr/local
# Isso torna fácil copiar apenas os pacotes para a imagem final (COPY --from=builder)
# --no-cache-dir: não guarda cache do pip (reduz tamanho do estágio builder)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Estágio 2: final ──────────────────────────────────────────────────────────
# Imagem limpa — começa do zero, sem compiladores, sem cache, sem resíduos de build.
# python:3.11-slim ≈ 130MB — equilíbrio certo para projetos que usam scikit-learn/numpy
# NÃO usar python:3.11-alpine: wheels de ML compilados para glibc falham no musl libc do Alpine
FROM python:3.11-slim

WORKDIR /app

# Copia APENAS os pacotes instalados do estágio builder
# --from=builder: busca no estágio anterior (descartado após este passo)
COPY --from=builder /install /usr/local

# Copia o código da aplicação
# O .dockerignore garante que __pycache__, .env, tests/, *.pkl etc. ficam de fora
COPY . .

# ── Segurança: usuário não-root ───────────────────────────────────────────────
# Por padrão os processos rodam como root dentro do contêiner — desnecessariamente poderoso.
# A API só precisa ler arquivos e servir HTTP.
# addgroup/adduser --system: cria contas de sistema sem senha e sem shell de login
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Troca para o usuário sem privilégios
# Todas as instruções seguintes (CMD) rodam como appuser
USER appuser

# Documenta que a aplicação escuta na porta 8000
# EXPOSE é documentação — o -p no docker run (ou ports: no Compose) é que abre a porta
EXPOSE 8000

# Forma de lista JSON: não usa shell intermediário (importante para propagação de sinais)
# --host 0.0.0.0: escuta em todas as interfaces do contêiner
#   sem isso, uvicorn ouve só em 127.0.0.1 (loopback interno) e o roteamento de portas falha
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
