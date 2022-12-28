from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str = "<None>"

    class Config:
        env_file = ".env"


settings = Settings()
