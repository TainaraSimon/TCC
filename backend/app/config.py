from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    groq_api_key: str
    jwt_secret: str
    jwt_expiracao_minutos: int = 60 * 24  # 1 dia

    modelo_transcricao: str = "whisper-large-v3"
    modelo_analise: str = "qwen/qwen3.8-27b"
    cors_origins: list[str] = ["http://localhost:9000"]


settings = Settings()