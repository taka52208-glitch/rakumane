from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    gumroad_access_token: str = ""
    frontend_url: str = "https://rakumane.vercel.app"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
