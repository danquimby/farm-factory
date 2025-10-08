from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
from loguru import logger

from .config import settings


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, time_window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old requests
        self.requests[client_ip] = [
            req_time
            for req_time in self.requests.get(client_ip, [])
            if current_time - req_time < self.time_window
        ]

        if len(self.requests.get(client_ip, [])) >= self.max_requests:
            from starlette.responses import JSONResponse

            return JSONResponse(
                status_code=429, content={"detail": "Too many requests"}
            )

        self.requests.setdefault(client_ip, []).append(current_time)

        return await call_next(request)


def add_middleware(app: FastAPI):
    """
    Add all middleware to the FastAPI application.
    """
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host Middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS if settings.ALLOWED_HOSTS else ["*"],
    )

    # GZip Middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Custom Middleware
    app.add_middleware(LoggingMiddleware)

    # Rate limiting only in production
    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            RateLimitMiddleware,
            max_requests=settings.RATE_LIMIT_PER_MINUTE,
            time_window=60,
        )
