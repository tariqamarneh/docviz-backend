from bson.objectid import ObjectId
from fastapi import UploadFile, HTTPException, status

from app.common.models.files import File
from app.common.logging.logger import mongo_logger
from app.common.database import file_collection, grid_fs


async def add_file(file: UploadFile, user_id: str, session_id: str):
    file_name = file.filename
    content_type = file.content_type
    file_id = await grid_fs.upload_from_stream(
        filename=file_name,
        source=file.file,
        metadata={
            "user_id": ObjectId(user_id),
            "session_id": ObjectId(session_id),
            "content_type": content_type,
        },
    )
    return file_id


async def delete_file(file_id: str):
    try:
        await grid_fs.delete(file_id=ObjectId(file_id))
    except Exception as e:
        mongo_logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No file found with id: {file_id}, error {e}",
        )


async def get_file(file_id: str):
    file = await file_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        return File(id=str(file["_id"]), **file)
    return None


async def get_file_binary(file_id: str):
    cursor = grid_fs.find({"_id": ObjectId(file_id)})
    data = None
    while await cursor.fetch_next:
        grid_out = cursor.next_object()
        data = await grid_out.read()
    return data
