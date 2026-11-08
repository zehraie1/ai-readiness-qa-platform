"""Consistent error envelope: {code, message, details, request_id}."""

import logging
from enum import StrEnum
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.request_id import request_id_var

logger = logging.getLogger("app.errors")


class ErrorCode(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOO_MANY_ATTEMPTS = "TOO_MANY_ATTEMPTS"
    FORBIDDEN = "FORBIDDEN"
    CSRF_REJECTED = "CSRF_REJECTED"
    NOT_FOUND = "NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    BAD_REQUEST = "BAD_REQUEST"
    TRACK_NOT_FOUND = "TRACK_NOT_FOUND"
    ATTEMPT_NOT_FOUND = "ATTEMPT_NOT_FOUND"
    QUESTION_NOT_IN_ATTEMPT = "QUESTION_NOT_IN_ATTEMPT"
    ATTEMPT_CLOSED = "ATTEMPT_CLOSED"
    ATTEMPT_INCOMPLETE = "ATTEMPT_INCOMPLETE"
    RESULTS_NOT_AVAILABLE = "RESULTS_NOT_AVAILABLE"
    NO_PUBLISHED_TEMPLATE = "NO_PUBLISHED_TEMPLATE"
    NO_SCORING_POLICY = "NO_SCORING_POLICY"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_OPTION = "INVALID_OPTION"
    HTTP_ERROR = "HTTP_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: Any = None
    request_id: str


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        code: ErrorCode,
        message: str,
        details: Any = None,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(message)
        self.headers = headers or {}
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def current_request_id(request: Request | None = None) -> str:
    if request is not None:
        rid = getattr(request.state, "request_id", None)
        if rid:
            return rid
    return request_id_var.get()


def error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: Any = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    rid = current_request_id(request)
    body = ErrorEnvelope(code=code, message=message, details=details, request_id=rid)
    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(),
        headers={**(headers or {}), "X-Request-ID": rid},
    )


_HTTP_CODES = {
    400: ErrorCode.BAD_REQUEST,
    401: ErrorCode.UNAUTHENTICATED,
    403: ErrorCode.FORBIDDEN,
    404: ErrorCode.NOT_FOUND,
    405: ErrorCode.METHOD_NOT_ALLOWED,
}
_HTTP_MESSAGES = {
    400: "The request could not be processed.",
    401: "Authentication required.",
    403: "You do not have permission to perform this action.",
    404: "The requested resource was not found.",
    405: "Method not allowed.",
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):
        return error_response(request, exc.status_code, exc.code, exc.message, exc.details, exc.headers)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError):
        # Never echo submitted input back to the client.
        details = [
            {"loc": list(err.get("loc", [])), "msg": err.get("msg"), "type": err.get("type")}
            for err in exc.errors()
        ]
        return error_response(request, 422, ErrorCode.VALIDATION_ERROR, "The request is invalid.", details)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        code = _HTTP_CODES.get(exc.status_code, ErrorCode.HTTP_ERROR)
        message = _HTTP_MESSAGES.get(exc.status_code, "The request could not be completed.")
        return error_response(request, exc.status_code, code, message)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        logger.exception("Unhandled error")
        return error_response(request, 500, ErrorCode.INTERNAL_ERROR, "An unexpected error occurred.")
