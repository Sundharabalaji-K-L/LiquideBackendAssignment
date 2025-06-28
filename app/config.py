from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib


class Config(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 10
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = 7

    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent.parent/".env"
    )


settings = Config()

