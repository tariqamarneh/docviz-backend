from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class File(BaseModel):
    id: Optional[str]
    filename:str
    metadata: Any
    chunkSize:Any
    length:Any
    uploadDate: datetime