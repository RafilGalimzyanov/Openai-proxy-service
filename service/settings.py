from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class Token(BaseSettings):
    value: str = Field(..., env='TOKEN_VALUE')


class DatabaseSettings(BaseSettings):
    user: str = Field(..., env='DB__USER')
    password: str = Field(..., env='DB__PASSWORD')
    host: str = Field(..., env='DB__HOST')
    port: int = Field(..., env='DB__PORT')
    name: str = Field(..., env='DB__NAME')


token = Token(_env_file='../.env', _env_file_encoding='utf-8')
db = DatabaseSettings(_env_file='../.env', _env_file_encoding='utf-8')
