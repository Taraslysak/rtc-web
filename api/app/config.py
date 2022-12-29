from pydantic import BaseSettings


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str = "<None>"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str = "dummy_pass"
    JWT_SECRET: str = "dummy_secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
