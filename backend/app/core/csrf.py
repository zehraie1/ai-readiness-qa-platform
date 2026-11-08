"""CSRF defence for cookie sessions: unsafe API requests must come from an allowed Origin."""

from urllib.parse import urlsplit

from starlette.requests import Request

from app.core.errors import ErrorCode, error_response

UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _origin_of(url: str) -> str | None:
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return None
    return f"{parts.scheme}://{parts.netloc}"


class OriginCheckMiddleware:
    def __init__(self, app, allowed_origins: list[str], cookie_name: str):
        self.app = app
        self.allowed = set(allowed_origins)
        self.cookie_name = cookie_name

    async def __call__(self, scope, receive, send):
        if (
            scope["type"] == "http"
            and scope["method"] in UNSAFE_METHODS
            and scope["path"].startswith("/api/")
        ):
            request = Request(scope)
            origin = request.headers.get("origin")
            if origin is None and request.headers.get("referer"):
                origin = _origin_of(request.headers["referer"])
            has_session_cookie = self.cookie_name in request.cookies
            rejected = (origin is not None and origin.rstrip("/") not in self.allowed) or (
                origin is None and has_session_cookie
            )
            if rejected:
                response = error_response(
                    request, 403, ErrorCode.CSRF_REJECTED, "Request origin is not allowed."
                )
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)
