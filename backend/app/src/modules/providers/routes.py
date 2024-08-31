from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import Provider, Spot, User, Alias
from app.limiter import limiter
from app.src.common.dtos import SpotData, ProviderData
from app.src.middleware.token_auth import provider_auth
from app.src.modules.providers.exceptions import MaxSpotIsReached
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
    if provider.spots + 1 > provider.max_spots:
        raise MaxSpotIsReached
    spot_service_user = User(
        role=Roles.spotUser.value
    )

    session.add(spot_service_user)
    await session.commit()

    spot = Spot(
        account=spot_service_user.id,
        provider_id=provider.id
    )
    session.add(spot)
    await session.commit()
    alias = Alias(base=spot.id)
    session.add(alias)

    spot_service_user.set_data(
        spot.service_user_data
    )
    session.add(spot_service_user)
    provider.spots += 1
    (await provider.spots_list).append(spot)
    await session.commit()
    return await SpotData.by_model(session, spot)


@router.get("/me")
@limiter.limit("3/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        provider: Provider = Depends(provider_auth)
) -> ProviderData:
    response: ProviderData = await ProviderData.by_model(
        session,
        provider
    )
    return response


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
    provider.name = data.name if data.name else provider.name
    provider.description = data.description if data.description else provider.description
    await session.commit()
    response: ProviderData = await ProviderData.by_model(
        session,
        provider
    )
    return response
