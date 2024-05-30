from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from app.config import ALLOWED_FILE_TYPES
from app.auth.dependencies import user_dependency
from app.common.schemas.file_schema import Metadata
from app.services.uploadfile import add_file, delete_file, get_file

router = APIRouter()


@router.post("/upload", response_model=Metadata)
async def uploadfile(user: user_dependency, file: UploadFile = File(...)):
    user_id = user.id
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )
    file_id = await add_file(file=file, user_id=user_id)
    if file_id:
        return Metadata(user_id=user_id, filename=file.filename, content_type=file.content_type)
    
    raise HTTPException(status_code=500, detail="File upload failed")

@router.delete("/delete/{file_id}")
async def deletefile(user: user_dependency, file_id:str):
    file = await get_file(file_id)
    if not file or file.metadata['user_id'] != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    await delete_file(file_id)
    return JSONResponse(
        content="file deleted successfully", status_code=status.HTTP_200_OK
    )

@router.get("/get/{file_id}")
async def getfile(user: user_dependency, file_id:str):
    file = await get_file(file_id)
    if not file or file.metadata['user_id'] != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return file