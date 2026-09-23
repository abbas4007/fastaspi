from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./fastApiToDoApp.db"
    APP_NAME: str = "FastAPI ToDo App"
    DEBUG: bool = True


settings = Settings()