import time
from typing import Dict
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.schemas.logging_schema import RouteLoggingSchema
from app.common.logging.logger import mongo_route_logger


class Middleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: RouteLoggingSchema):
        mongo_route_logger.info(message.model_dump())

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        if (
            request.url.path not in ["/docs", "/openapi.json", '/favicon.ico']
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
            RouteLoggingSchema(
                method=method, url=path, host=client_ip, process_time=process_time
            )
        )

        return response
