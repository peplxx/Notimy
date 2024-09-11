from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.connection import get_session
from app.data.db.models import Provider
from app.data.db.repositories import ProviderRepository
from app.src.common.dtos import SpotData, ProviderData
from app.src.limiter import limiter
from app.src.middleware.token_auth import provider_auth
from app.src.modules.providers.exceptions import MaxSpotIsReached
from app.src.modules.providers.logic import create_spot
from app.src.modules.providers.schemas import ProviderUpdateData

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.post(
    "/new_spot",
    responses={
        **MaxSpotIsReached.responses
    }
)
async def create_new_spot(
        session: AsyncSession = Depends(get_session),
        provider: Provider = Depends(provider_auth)
) -> SpotData:
    spot = await create_spot(session, provider)
    return await SpotData.by_model(session, spot)


@router.get("/me")
@limiter.limit("3/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        provider: Provider = Depends(provider_auth)
) -> ProviderData:
    return await ProviderData.by_model(session, provider)


@router.put(
    "/update",
    response_model=ProviderData,
)
@limiter.limit("3/second")
async def update_providers_data(
        request: Request,
        data: ProviderUpdateData = Body(...),
        session: AsyncSession = Depends(get_session),
        provider: Provider = Depends(provider_auth)
) -> ProviderData:
    provider_repo = ProviderRepository(session)
    await provider_repo.update(provider=provider, name=data.name, description=data.description)
    return await ProviderData.by_model(session, provider)
