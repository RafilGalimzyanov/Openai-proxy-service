from fastapi import FastAPI
from starlette import status
from starlette.responses import Response, FileResponse

from service.database import get_data
from service.models import EmbeddingRequest, ChatCompletionRequest, User
from service.process import user_is_valid, create_embeddings_process, chat_completions, is_admin

app = FastAPI(
    title="Proxy service",
    description="Proxy service",
    version="0.3.0",
    debug=True,
    root_path=""
)


@app.post("/api/{login}:{password}/embeddings", response_model=None)
async def create_embeddings(
        login: str,
        password: str,
        data: EmbeddingRequest
):
    if not await user_is_valid(login, password):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await create_embeddings_process(data, login)


@app.post("/api/{login}:{password}/chat/completions", response_model=None)
async def chat(
        login: str,
        password: str,
        data: ChatCompletionRequest
):
    if not await user_is_valid(login, password):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await chat_completions(data, login)


@app.get("/api/logs")
async def get_logs(user: User):
    if not await is_admin(user):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not admin!")

    filename = get_data()
    return FileResponse(path=filename, media_type="text/csv", filename=filename)
