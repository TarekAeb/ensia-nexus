from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/fastapi_research_lab"
    SECRET_KEY: str
    DB_ECHO: bool = False
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
