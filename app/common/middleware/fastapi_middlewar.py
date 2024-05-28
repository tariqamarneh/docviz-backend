import time
from typing import Dict
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.schemas.logging_schema import LoggingSchema
from app.common.logging.logger import file_logging


class Middleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: LoggingSchema):
        file_logging.info(message)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        if (
            request.url.path not in ["/docs", "/openapi.json"]
            and current_time - self.rate_limit_records[client_ip] < 1
        ):
            return Response(content="Rate limit exceeded", status_code=429)

        self.rate_limit_records[client_ip] = current_time
        method = request.method
        path = request.url.path

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        custom_headers = {"X-Process-Time": str(process_time)}
        for header, value in custom_headers.items():
            response.headers.append(header, value)

        await self.log_message(
            LoggingSchema(
                method=method, url=path, host=client_ip, process_time=process_time
            )
        )

        return response
