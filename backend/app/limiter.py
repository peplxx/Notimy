__all__ = ["limiter", "NoOpLimiter"]

from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse


class NoOpLimiter:
    def limit(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator


from app.config import get_settings


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded"},
    )


if get_settings().is_test:
    exit(0)
    limiter = NoOpLimiter()
else:
    limiter = Limiter(
        key_func=get_remote_address,
        # default_limits=["200 per day", "50 per hour"]
    )
