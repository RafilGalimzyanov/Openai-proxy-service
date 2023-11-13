import json

from starlette.responses import Response

from service.chatgpt import send_message_gpt
from service.database import add_history
from service.models import Message, User, ErrorMessage


async def user_is_valid(login: str, password: str) -> bool:
    with open("secrets.json", "r") as secrets_file:
        secrets = json.loads(secrets_file.read())

    for lg, pw in secrets.items():
        if login == lg and password == pw:
            return True

    return False


async def send_message(user: User, message: Message):
    response = await send_message_gpt(message)

    if type(response) is ErrorMessage:
        return Response(status_code=response.code, content=response.message)

    response = response.dict()
    tokens = response.get("usage").get("total_tokens")

    add_history(user.login, json.dumps(message.dict()), json.dumps(response), tokens)

    return response
