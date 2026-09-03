from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
    data_dir: str = "./data"
    admin_secret: str = "change_me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()