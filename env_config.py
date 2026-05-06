"""
env_config.py
=============
Cria ou atualiza o arquivo .env com as configurações do projeto.

Execute:
    python env_config.py

Você pode também editar o .env manualmente depois.
"""

from pathlib import Path

ENV_PATH = Path(".env")

VARIAVEIS = {
    # ── Aplicação ─────────────────────────────────────────────────────────────
    "APP_NAME":              ("Nome da API",                  "Bella Tavola API"),
    "APP_VERSION":           ("Versão",                       "1.0.0"),
    "DEBUG":                 ("Modo debug (true/false)",      "false"),
    "MAX_MESAS":             ("Número máximo de mesas",       "20"),
    "MAX_PESSOAS_POR_MESA":  ("Pessoas máximas por mesa",     "10"),
    # ── Hugging Face ─────────────────────────────────────────────────────────
    "HF_TOKEN":              ("Token Hugging Face (write)",   ""),
    "HF_REPO":               ("Repositório HF (user/repo)",   ""),
}


def criar_env():
    print("=" * 55)
    print("  Configuração do arquivo .env")
    print("  Pressione Enter para manter o valor padrão.")
    print("=" * 55)

    linhas = []
    for chave, (descricao, padrao) in VARIAVEIS.items():
        prompt = f"\n{descricao}"
        if padrao:
            prompt += f" [{padrao}]"
        prompt += ": "

        valor = input(prompt).strip()
        if not valor:
            valor = padrao

        linhas.append(f"{chave}={valor}")

    conteudo = "\n".join(linhas) + "\n"
    ENV_PATH.write_text(conteudo, encoding="utf-8")

    print(f"\n✅ Arquivo .env criado em: {ENV_PATH.resolve()}")
    print("\nConteúdo gerado:")
    for linha in linhas:
        chave = linha.split("=")[0]
        # Oculta tokens sensíveis no print
        if "TOKEN" in chave:
            print(f"  {chave}=****")
        else:
            print(f"  {linha}")


def mostrar_env():
    """Exibe o .env atual (sem mostrar tokens)."""
    if not ENV_PATH.exists():
        print("❌ .env não encontrado. Execute: python env_config.py")
        return
    print("\n📄 Configurações atuais (.env):")
    for linha in ENV_PATH.read_text().splitlines():
        if "TOKEN" in linha:
            chave = linha.split("=")[0]
            print(f"  {chave}=****")
        else:
            print(f"  {linha}")


if __name__ == "__main__":
    if ENV_PATH.exists():
        print(f"⚠️  .env já existe.")
        mostrar_env()
        resposta = input("\nDeseja recriar? (s/N): ").strip().lower()
        if resposta != "s":
            print("Nenhuma alteração feita.")
        else:
            criar_env()
    else:
        criar_env()
