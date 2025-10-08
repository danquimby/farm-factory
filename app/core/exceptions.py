from fastapi import FastAPI, HTTPException as FastAPIHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette import status
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class HTTPException(FastAPIHTTPException):
    def __init__(
            self,
            status_code: int,
            detail: Any = None,
            headers: Dict[str, str] | None = None,
            error_code: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handle validation errors and return a consistent error format.
    """
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors(),
            }
        },
    )


async def http_exception_handler(request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions and return a consistent error format.
    """
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": getattr(exc, "error_code", "HTTP_ERROR"),
                "message": exc.detail,
                "details": None,
            }
        },
        headers=exc.headers,
    )


async def general_exception_handler(request, exc: Exception):
    """
    Handle all other exceptions and return a consistent error format.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
                "details": str(exc) if settings.DEBUG else None,
            }
        },
    )


def setup_exception_handlers(app: FastAPI):
    """
    Setup custom exception handlers for the application.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
