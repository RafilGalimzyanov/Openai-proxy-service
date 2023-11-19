from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    login: str
    password: str


class Message(BaseModel):
    dialog_contexts: List[dict]
    configs: List[dict]


class ErrorMessage(BaseModel):
    code: int = Field(..., title="Error code")
    message: str = Field(..., title="Error text")
