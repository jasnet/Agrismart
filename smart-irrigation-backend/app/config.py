from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./irrigation.db"
    DEFAULT_ET0: float = 5.0
    # set to your weather API key if you integrate one later
    WEATHER_API_KEY: str | None = None
    SECRET_KEY: str = "supersecretkey" # Adding fallback if missing

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()