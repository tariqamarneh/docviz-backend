from bson.objectid import ObjectId
from datetime import datetime, timedelta, UTC

from app.common.models.sessions import Session
from app.common.database import session_collection, user_collection


async def create_session(user_id: str, data: dict, expires_in_minutes: int) -> Session:
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_in_minutes)
    session_data = {
        "user_id": user_id,
        "data": data,
        "created_at": datetime.now(UTC),
        "expires_at": expires_at,
    }
    result = await session_collection.insert_one(session_data)
    session = Session(id=str(result.inserted_id), **session_data)
    return session


async def get_session(session_id: str) -> Session:
    session = await session_collection.find_one({"_id": ObjectId(session_id)})
    if session:
        return Session(id=str(session["_id"]), **session)
    return None


async def delete_session(session_id: str):
    await session_collection.delete_one({"_id": ObjectId(session_id)})


async def delete_sessions_by_user_id(user_id: str):
    await session_collection.delete_many({"user_id": user_id})


async def get_sessions_by_email(email: str) -> list[Session]:
    sessions = []
    user = await user_collection.find_one({"email": email})
    user_id = user["_id"]
    if user_id:
        async for session in session_collection.find({"user_id": str(user_id)}):
            sessions.append(Session(id=str(session["_id"]), **session))
        return sessions
    return None
