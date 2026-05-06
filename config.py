from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bella Tavola API"
    app_version: str = "1.0.0"
    app_description: str = "API do restaurante Bella Tavola 🍝"
    debug: bool = False
    max_mesas: int = 20
    max_pessoas_por_mesa: int = 10
    hf_token: str = ""           # Hugging Face token (preencha no .env)
    hf_repo: str = ""            # ex: "seu-usuario/bella-tavola-model"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
