from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    login: str
    password: str


class EmbeddingRequest(BaseModel):
    input: list
    model: str
    encoding_format: Optional[str] = "float"

    class Config:
        extra = 'allow'


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[dict]

    class Config:
        extra = 'allow'
