from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.config import MONGO_CONNECTION_STRING


def get_connection():
    connection = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    return connection


def get_gridFS_collection():
    collection = AsyncIOMotorGridFSBucket(
        get_connection()["docViz"], bucket_name="files"
    )
    return collection
