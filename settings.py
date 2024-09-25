from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    website_url: str
    token: str
    redis_host: str
    redis_port: int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')