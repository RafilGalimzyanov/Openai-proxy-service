from openai import OpenAI, APIConnectionError, AuthenticationError, BadRequestError, RateLimitError
from starlette import status

from service.models import Message, ErrorMessage
from service.settings import token


client = OpenAI(api_key=token.value)


async def send_message_gpt(message: Message):
    try:
        return client.completions.create(**message.dict())
    except APIConnectionError as e:
        return ErrorMessage(code=e.code, message=f"API Connection Error: {e}")
    except AuthenticationError as e:
        return ErrorMessage(code=e.status_code, message=f"Authentication Error: {e}")
    except BadRequestError as e:
        return ErrorMessage(code=e.status_code, message=f"Bad Request Error: {e}")
    except RateLimitError as e:
        return ErrorMessage(code=e.status_code, message=f"Rate Limit Error: {e}")
    except Exception as e:
        return ErrorMessage(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Error: {e}")
