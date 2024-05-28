from pydantic import BaseModel

class LoggingSchema(BaseModel):
    method:str
    url:str
    host:str
    process_time:float