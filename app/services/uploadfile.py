from bson.objectid import ObjectId
from fastapi import UploadFile, HTTPException, status

from app.common.database import file_collection, grid_fs
from app.common.models.files import File


async def add_file(file: UploadFile, user_id: str):
    file_name = file.filename
    content_type = file.content_type
    file_id = await grid_fs.upload_from_stream(
        filename=file_name,
        source=file.file,
        metadata={"user_id": user_id, "content_type": content_type},
    )
    return file_id


async def delete_file(file_id: str):
    try:
        await grid_fs.delete(file_id=ObjectId(file_id))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No file found with id: {file_id}, error {e}",
        )


async def get_file(file_id: str):
    file = await file_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        return File(id=str(file["_id"]), **file)
    return None
