# Imagem base: Python 3.11 mínimo (Debian slim)
# python:3.11-slim ≈ 130MB — equilíbrio certo para projetos que usam scikit-learn/numpy
# NÃO usar python:3.11-alpine: pacotes de ML compilados para glibc falham no musl libc do Alpine
FROM python:3.11-slim

# Diretório de trabalho dentro do contêiner
# Todos os comandos seguintes (COPY, RUN, CMD) operam relativos a /app
WORKDIR /app

# Copia APENAS o requirements.txt primeiro — antes do código
# Motivo: cache de layers. O pip install só reexecuta quando requirements.txt muda.
# Se o COPY . . viesse antes, qualquer alteração em qualquer .py invalidaria o pip install.
COPY requirements.txt .

# Instala as dependências dentro da imagem
# --no-cache-dir: não guarda cache do pip na imagem (reduz o tamanho final)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código DEPOIS das dependências
# Mudanças no código não invalidam a camada do pip install
COPY . .

# Documenta que a aplicação escuta na porta 8000
# EXPOSE não abre a porta — o -p no docker run é que faz isso
EXPOSE 8000

# Comando padrão ao iniciar o contêiner
# Forma de lista JSON: não usa shell intermediário (mais correto para sinais do SO)
# --host 0.0.0.0: escuta em todas as interfaces de rede do contêiner
#   sem isso, uvicorn ouve em 127.0.0.1 (loopback interno) e o -p não consegue rotear
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
