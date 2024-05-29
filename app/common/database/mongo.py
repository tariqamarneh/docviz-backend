from motor.motor_asyncio import AsyncIOMotorClient

from app.config import MONGO_CONNECTION_STRING


def get_connection():
    connection = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    return connection
