import json
import os

import aiohttp
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from service.database import add_history
from service.models import EmbeddingRequest, ChatCompletionRequest, User

ENDPOINTS = {
    "embeddings": "/embeddings",
    "chat_completions": "/chat/completions",
}
BASE_URL = os.getenv("OPENAI_BASE_URL")
API_TOKEN = os.getenv('OPENAI_API_KEY')


async def user_is_valid(login: str, password: str) -> bool:
    with open("secrets.json", "r") as secrets_file:
        secrets = json.loads(secrets_file.read())

    for lg, pw in secrets.items():
        if login == lg and password == pw:
            return True

    return False


async def is_admin(user: User):
    with open("admins.json", "r") as secrets_file:
        secrets = json.loads(secrets_file.read())

    for lg, pw in secrets.items():
        if user.login == lg and user.password == pw:
            return True

    return False


async def create_embeddings_process(data: EmbeddingRequest, login: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + ENDPOINTS["embeddings"], json=jsonable_encoder(data),
                                headers={"Authorization": f"Bearer {API_TOKEN}"}) as response:
            if response.status == 200:
                result = await response.json()
                add_history(login, data.input, result, result["usage"]["total_tokens"])
                return result
            else:
                raise aiohttp.ClientResponseError(status=response.status, message="Error from OpenAI API")


async def chat_completions(request_data: ChatCompletionRequest, login):

    if not request_data.messages:
        raise HTTPException(status_code=400, detail="At least one message is required.")

    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

        async with session.post(
                BASE_URL + ENDPOINTS["chat_completions"], json=request_data.dict(), headers=headers
        ) as response:
            if response.status == 200:
                result = await response.json()
                add_history(login, request_data.messages, result, result["usage"]["total_tokens"])
                return result
            else:
                raise HTTPException(status_code=response.status, detail="Error from OpenAI API")
