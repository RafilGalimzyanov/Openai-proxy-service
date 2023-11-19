import json

from openai import OpenAI, APIConnectionError, AuthenticationError, BadRequestError, RateLimitError
from starlette import status

from service.models import Message, ErrorMessage


DEFAULT_CONFIGS = {
    "text-davinci-003": json.load(open("./generative_configs/openai-text-davinci-003.json", "r")),
    "gpt-3.5-turbo": json.load(open("./generative_configs/openai-chatgpt.json", "r")),
    "gpt-3.5-turbo-16k": json.load(open("./generative_configs/openai-chatgpt.json", "r")),
    "gpt-4": json.load(open("./generative_configs/openai-chatgpt.json", "r")),
    "gpt-4-32k": json.load(open("./generative_configs/openai-chatgpt.json", "r")),
}
DEFAULT_MODEL = 'gpt-3.5-turbo'
CHAT_COMPLETION_MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"]

client = OpenAI()


def check_model_is_valid(model: str):
    if model.replace(" ", "") in DEFAULT_CONFIGS.keys():
        return model

    return DEFAULT_MODEL


def handle_openai_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIConnectionError as e:
            return ErrorMessage(code=e.code, message=f"API Connection Error: {e}")
        except AuthenticationError as e:
            return ErrorMessage(code=e.status_code, message=f"Authentication Error: {e}")
        except BadRequestError as e:
            return ErrorMessage(code=e.status_code, message=f"Bad Request Error: {e}")
        except RateLimitError as e:
            return ErrorMessage(code=e.status_code, message=f"Rate Limit Error: {e}")
        except Exception as e:
            return ErrorMessage(code=status.HTTP_404_NOT_FOUND, message=f"Error: {e}")

    return wrapper


@handle_openai_exception
def send_message_gpt(message: Message):
    generation_params = {}
    model = DEFAULT_MODEL

    if model := message.configs[0].pop("model"):
        model = check_model_is_valid(model)
    if configs := message.configs:
        generation_params = configs[0]

    return client.chat.completions.create(model=model, messages=message.dialog_contexts, **generation_params)
