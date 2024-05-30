from pydantic import BaseModel

class Metadata(BaseModel):
    user_id: str
    filename: str
    content_type: str
