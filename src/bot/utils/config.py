from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(env_file=".env.bot")

settings = Settings()