from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    login: str
    password: str


class Message(BaseModel):
    dialog_contexts: List[dict]
    configs: List[dict]


class Document(BaseModel):
    rows: List[dict]


class LangChainAnswer(BaseModel):
    prompt_template: str
    input_variables: list
    question: str


class ErrorMessage(BaseModel):
    code: int = Field(..., title="Error code")
    message: str = Field(..., title="Error text")
