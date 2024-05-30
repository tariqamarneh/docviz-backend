from app.common.database.mongo import get_connection, get_gridFS_collection

user_collection = get_connection()["docViz"]["users"]
password_collection = get_connection()["docViz"]["passwords"]
session_collection = get_connection()["docViz"]['sessions']
file_collection = get_connection()['docViz']["files.files"]
grid_fs = get_gridFS_collection()

async def create_indexes():
    await session_collection.create_index("user_id")
    await session_collection.create_index("expires_at", expireAfterSeconds=0)
