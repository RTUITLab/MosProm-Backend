from pydantic import BaseSettings


class Settings(BaseSettings):
    # database settings
    database_url: str

    # main app settings
    debug: bool = False
    secret_key: str = 'a26cc7f6b827afaa'
    access_token_expires_minutes: int = 60

    # proxy settings
    root_path: str = ''

    class Config:
        env_file = ".env"
