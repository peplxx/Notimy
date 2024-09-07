__all__ = ['app']

import logging
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.limiter import limiter, rate_limit_exceeded_handler, NoOpLimiter
from app.src import docs
from app.src.lifespan import lifespan
from app.src.middleware.login_manager import NotAuthenticatedException
from app.src.routers import routers

settings = get_settings()

app = FastAPI(
    title=docs.TITLE,
    summary=docs.SUMMARY,
    description=docs.DESCRIPTION,
    version=docs.VERSION,
    contact=docs.CONTACT_INFO,
    license_info=docs.LICENSE_INFO,
    openapi_tags=docs.TAGS_INFO,
    lifespan=lifespan,
    docs_url=settings.docs_path,
    redoc_url=None,
)

for router in routers:
    app.include_router(prefix=settings.PATH_PREFIX, router=router)

origins = [
    "http://localhost:3000",
    "https://localhost",
    "http://test"
    "https://notimy.ru"
]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if not settings.is_test:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(NotAuthenticatedException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(settings.PATH_PREFIX + f"/login?next={(request.url.path)}")


if get_settings().is_dev:
    from app.src.logging import logger

    logger.warning("Enable sqlalchemy logging")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

if get_settings().is_test:
    log_dir = "logs/test"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log")

    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        datefmt='%Y-%m-%d %H:%M:%S',  # Date format
        handlers=[
            logging.FileHandler(log_filename),  # Log to a file
            logging.StreamHandler()  # Log to console
        ]
    )
    logger = logging.getLogger("[TEST] app")
    logger.warning("Enable sqlalchemy logging")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@app.get(settings.PATH_PREFIX + '/', tags=["System"], include_in_schema=False)
@limiter.limit("2/second")
async def ping(request: Request):
    return {
        "message": "Hello it's Notimy!"
    }
