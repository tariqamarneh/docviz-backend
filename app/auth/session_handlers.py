from bson.objectid import ObjectId
from datetime import datetime, timedelta, UTC

from app.common.models.sessions import Session
from app.common.database import session_collection, user_collection


async def create_session(user_id: str, data: dict, expires_in_minutes: int) -> Session:
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_in_minutes)
    session_data = {
        "user_id": ObjectId(user_id),
        "data": data,
        "created_at": datetime.now(UTC),
        "expires_at": expires_at,
    }
    result = await session_collection.insert_one(session_data)
    session = Session(
        id=str(result.inserted_id),
        user_id=str(session_data["user_id"]),
        data=session_data["data"],
        created_at=session_data["created_at"],
        expires_at=session_data["expires_at"],
    )
    return session


async def get_session(session_id: str) -> Session:
    session = await session_collection.find_one({"_id": ObjectId(session_id)})
    if session:
        return Session(
            id=str(session["_id"]),
            user_id=str(session["user_id"]),
            data=session["data"],
            created_at=session["created_at"],
            expires_at=session["expires_at"],
        )
    return None


async def delete_session(session_id: str):
    await session_collection.delete_one({"_id": ObjectId(session_id)})


async def delete_sessions_by_user_id(user_id: str):
    await session_collection.delete_many({"user_id": ObjectId(user_id)})


async def get_sessions_by_user_id(user_id: str) -> list[Session]:
    sessions = []
    async for session in session_collection.find({"user_id": ObjectId(user_id)}):
        sessions.append(
            Session(
                id=str(session["_id"]),
                user_id=str(session["user_id"]),
                data=session["data"],
                created_at=session["created_at"],
                expires_at=session["expires_at"],
            )
        )
    if sessions:
        return sessions
    return None


async def update_session(session_id: str, data: dict):
    await session_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"data": data}},
    )


async def update_session_insights(session_id: str, data: str):
    await session_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"data.insights": data}},
    )
