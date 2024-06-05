from typing import Dict
from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    data: Dict
    expires_in_minutes: int
