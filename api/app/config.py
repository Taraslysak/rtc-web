from pydantic import BaseSettings


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str = "<None>"
    DATABASE_URI: str = "UNKNOWN_HOST"
    DEV_DATABASE_URI: str = "UNKNOWN_DEV_HOST"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    WS_TOKEN_EXPIRE_MINUTES: int = 1
    JWT_SECRET: str = "UNSET"

    class Config:
        env_file = [".env", ".env.prod"]


settings = Settings()
