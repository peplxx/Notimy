from app.src.modules.providers import router as providers_router
from app.src.modules.root import router as root_router
from app.src.modules.spots import router as spots_router
from app.src.modules.users import router as users_router
from app.src.modules.webpush import router as webpush_router
from app.src.modules.telegram import router as telegram_router

routers = [
    root_router,
    providers_router,
    spots_router,
    users_router,
    webpush_router,
    telegram_router,

]

__all__ = [
    "routers"
]
