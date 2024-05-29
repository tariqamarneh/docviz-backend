from pydantic import BaseModel
from datetime import datetime


class RouteLoggingSchema(BaseModel):
    method: str
    url: str
    host: str
    process_time: float


class LoggingSchema(BaseModel):
    when: datetime
    filename: str
    funcName: str
    levelname: str
    message: str
