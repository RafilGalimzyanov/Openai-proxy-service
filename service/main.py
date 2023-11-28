from typing import Optional, Dict

from fastapi import FastAPI, UploadFile, File
from starlette import status
from starlette.responses import Response, FileResponse

from service.database import get_data
from service.models import Message, User
from service.process import user_is_valid, send_message, create_langchain_answer, create_langchain_vb

app = FastAPI(
    title="Proxy service",
    description="Proxy service",
    version="0.3.0",
    debug=True,
    root_path="/api"
)


@app.post("/api/openai/chat", response_model=None)
async def chat(
        user: User,
        message: Message
):
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await send_message(user, message)


@app.post("/api/langchain/vector_base/{login}:{password}", response_model=None)
async def create_vectore_base(
        login: str,
        password: str,
        file_content: Optional[UploadFile] = File(...)
):
    user = User(login=login, password=password)
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await create_langchain_vb(user, file_content)


@app.post("/api/langchain/query", response_model=None)
async def create_answer(
        user: User,
        config: Dict[str, Optional[str]],
):
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await create_langchain_answer(user, config)


@app.get("/api/logs")
async def get_logs():
    filename = get_data()
    return FileResponse(path=filename, media_type="text/csv", filename=filename)
