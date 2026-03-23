from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Research Lab API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/fastapi_research_lab"
    DB_ECHO: bool = False
    
    CORS_ORIGINS: list[str] = ["*"]
    
    # Cookie settings
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
