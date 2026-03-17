from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/fastapi_research_lab"
    SECRET_KEY: str = "your-secret-key-here"

    class Config:
        env_file = ".env"


settings = Settings()
