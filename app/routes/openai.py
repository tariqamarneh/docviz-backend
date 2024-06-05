from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.auth.session_handlers import get_session
from app.auth.dependencies import user_dependency
from app.services.uploadfile import get_file
from app.routes.utils import send_message, send_message_insights
from app.common.schemas.openai_outout_schema import LLMSummaryOutputSchema

router = APIRouter()


@router.post("/get_summary")
async def get_summary(file_id: str, session_id: str, user: user_dependency):
    file = await get_file(file_id)
    if (
        not file
        or str(file.metadata["user_id"]) != user.id
        or str(file.metadata["session_id"]) != session_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return StreamingResponse(
        send_message(file_id=file_id, session_id=session_id), media_type="text/event-stream"
    )


@router.post("/get_insights")
async def get_insights(session_id:str, user: user_dependency):
    session = await get_session(session_id=session_id)
    if (
        not session
        or str(session.user_id) != str(user.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="session not found"
        )
    
    return StreamingResponse(
        send_message_insights(session_id=session_id), media_type="text/event-stream"
    )