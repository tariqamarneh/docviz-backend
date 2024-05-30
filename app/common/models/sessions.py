from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Session(BaseModel):
    id: Optional[str]
    user_id: str
    data: dict
    created_at: datetime
    expires_at: datetime
