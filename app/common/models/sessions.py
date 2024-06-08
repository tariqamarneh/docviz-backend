from pydantic import BaseModel
from typing import Any
from datetime import datetime


class Session(BaseModel):
    id: Any
    user_id: Any
    data: dict
    created_at: datetime
    expires_at: datetime
