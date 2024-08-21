__all__ = ['app']

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.src.middleware.login_manager import NotAuthenticatedException
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from urllib.parse import quote
from app.config import get_settings
from app.src import docs
from app.src.lifespan import lifespan
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
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(NotAuthenticatedException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(settings.PATH_PREFIX + f"/login?next={(request.url.path)}")


if settings.is_dev:
    # from src.logging_ import logger
    import logging

    logger = logging.getLogger("app")

    logger.warning("Enable sqlalchemy logging")
    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@app.get(settings.PATH_PREFIX + '/', tags=["System"], include_in_schema=False)
async def ping():
    return {
        "message": "Hello it's Notimy!"
    }

