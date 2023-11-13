from fastapi import FastAPI
from starlette import status
from starlette.responses import Response, FileResponse

from service.database import get_data
from service.models import Message, User
from service.process import user_is_valid, send_message


app = FastAPI(
    title="Proxy service",
    description="Proxy service",
    version="0.3.0",
    debug=True,
    root_path="/api"
)


@app.post("/api/chat", response_model=None)
async def chat(
        user: User,
        message: Message
):
    if not await user_is_valid(**user.dict()):
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="User is not valid!")

    return await send_message(user, message)


@app.get("/api/logs")
async def get_logs():
    filename = get_data()
    return FileResponse(path=filename, media_type="text/csv", filename=filename)
