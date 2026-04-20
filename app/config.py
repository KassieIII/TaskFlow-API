from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/taskflow"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
