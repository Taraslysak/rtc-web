from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str = "<None>"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str = "dummy_pass"

    class Config:
        env_file = ".env"


settings = Settings()
