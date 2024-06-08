from starlette.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, status

from app.services.uploadfile import get_file
from app.auth.session_handlers import get_session
from app.auth.dependencies import user_dependency
from app.common.logging.logger import mongo_logger
from app.routes.utils import send_message, send_message_insights

router = APIRouter()


@router.post("/get_summary")
async def get_summary(file_id: str, session_id: str, user: user_dependency):
    file = await get_file(file_id)
    if (
        not file
        or str(file.metadata["user_id"]) != user.id
        or str(file.metadata["session_id"]) != session_id
    ):
        mongo_logger.error("File not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return StreamingResponse(
        send_message(file_id=file_id, session_id=session_id),
        media_type="text/event-stream",
    )



@router.post("/get_insights")
async def get_insights(session_id: str, user: user_dependency):
    session = await get_session(session_id=session_id)
    if not session or str(session.user_id) != str(user.id):
        mongo_logger.error("Session not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="session not found"
        )
    return StreamingResponse(
        send_message_insights(session_id=session_id), media_type="text/event-stream"
    )
