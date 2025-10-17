from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    ENV: str = "dev"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
