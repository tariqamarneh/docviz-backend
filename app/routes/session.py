from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status

from app.common.models.sessions import Session
from app.auth.dependencies import user_dependency
from app.common.logging.logger import mongo_logger
from app.common.schemas.session_schema import CreateSessionRequest
from app.auth.session_handlers import (
    create_session,
    get_session,
    delete_session,
    get_sessions_by_user_id,
    update_session,
)

router = APIRouter()


@router.post("/create", response_model=Session)
async def create_user_session(
    request: CreateSessionRequest, current_user: user_dependency
):
    session = await create_session(
        user_id=current_user.id,
        data=request.data,
        expires_in_minutes=request.expires_in_minutes,
    )
    return session


@router.get("/get_by_id/{session_id}", response_model=Session)
async def get_user_session_by_session_id(
    session_id: str, current_user: user_dependency
):
    session = await get_session(session_id)
    if not session or session.user_id != current_user.id:
        mongo_logger.error("Session not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@router.get("/get_by_user_id", response_model=list[Session])
async def get_user_sessions_by_euser_id(user_id: str, current_user: user_dependency):
    sessions = await get_sessions_by_user_id(user_id)
    if not sessions or str(sessions[0].user_id) != current_user.id:
        mongo_logger.error("Session not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return sessions


@router.put("/edit/{session_id}")
async def update_user_session(
    session_id: str, data: dict, current_user: user_dependency
):
    session = await get_session(session_id)
    if not session or session.user_id != current_user.id:
        mongo_logger.error("Session not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    await update_session(session_id, data)
    return JSONResponse(
        content="Session updates successfully", status_code=status.HTTP_200_OK
    )


@router.delete("/delete/{session_id}")
async def delete_user_session(session_id: str, current_user: user_dependency):
    session = await get_session(session_id)
    if not session or session.user_id != current_user.id:
        mongo_logger.error("Session not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    await delete_session(session_id)
    return JSONResponse(
        content="Session deleted successfully", status_code=status.HTTP_200_OK
    )
