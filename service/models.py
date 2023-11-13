from pydantic import BaseModel, Field


class User(BaseModel):
    login: str
    password: str


class Message(BaseModel):
    prompt: str
    temperature: float = 0.5
    model: str = "text-davinci-003"
    max_tokens: int = 256
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0


class ErrorMessage(BaseModel):
    code: int = Field(..., title="Error code")
    message: str = Field(..., title="Error text")
