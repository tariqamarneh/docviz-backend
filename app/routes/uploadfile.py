from bson import ObjectId
from bson.errors import InvalidId

from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.config import ALLOWED_FILE_TYPES
from app.auth.dependencies import user_dependency
from app.common.logging.logger import mongo_logger
from app.common.database import session_collection
from app.common.schemas.file_schema import Metadata
from app.services.uploadfile import add_file, delete_file, get_file

router = APIRouter()


@router.post("/upload", response_model=Metadata)
async def uploadfile(
    user: user_dependency, session_id: str, file: UploadFile = File(...)
):
    user_id = user.id
    try:
        is_session = await session_collection.find_one(
            {"_id": ObjectId(session_id), "user_id": ObjectId(user_id)}
        )
        if not is_session:
            mongo_logger.error("Session not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )
    except InvalidId as e:
        mongo_logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session id"
        )
    except Exception as e:
        mongo_logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )

    if file.content_type not in ALLOWED_FILE_TYPES:
        mongo_logger.error("Unsupported file type")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )
    file_id = await add_file(file=file, user_id=user_id, session_id=session_id)
    if file_id:
        return Metadata(
            user_id=user_id,
            filename=file.filename,
            content_type=file.content_type,
            file_id=str(file_id),
        )
    mongo_logger.error("File upload failed")
    raise HTTPException(status_code=500, detail="File upload failed")


@router.delete("/delete/{file_id}")
async def deletefile(user: user_dependency, file_id: str):
    file = await get_file(file_id)
    if not file or str(file.metadata["user_id"]) != user.id:
        mongo_logger.error("File not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    await delete_file(file_id)
    return JSONResponse(
        content="file deleted successfully", status_code=status.HTTP_200_OK
    )


@router.get("/get/{file_id}")
async def getfile(user: user_dependency, file_id: str):
    file = await get_file(file_id)
    if not file or file.metadata["user_id"] != user.id:
        mongo_logger("File not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return file
