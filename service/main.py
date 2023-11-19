from fastapi import FastAPI
from starlette import status
from starlette.responses import Response, FileResponse

from service.database import get_data
from service.models import Message, User, Document, LangChainAnswer
from service.process import user_is_valid, send_message, create_langchain_vb, create_langchain_answer


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


@app.post("/api/langchain/vector_base", response_model=None)
async def create_vectore_base(
        user: User,
        document: Document
):
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await create_langchain_vb(user, document)


@app.post("/api/langchain/vector_base/query", response_model=None)
async def create_answer(
        user: User,
        config: LangChainAnswer
):
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await create_langchain_answer(user, config.prompt_template, config.input_variables, config.question)


@app.get("/api/logs")
async def get_logs():
    filename = get_data()
    return FileResponse(path=filename, media_type="text/csv", filename=filename)
