from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.connection import get_session
from app.src.common.dtos import ProviderData, SpotData
from app.src.middleware.token_auth import root_auth
from app.src.modules.root.exceptions import (
    ProviderDoesntExist,
    ImpossibleChange,
    SpotDoesntExist
)
from app.src.modules.root.logic import get_or_create_provider, change_provider_spot_limit, upsert_subscription_by_data
from app.src.modules.root.schemas import (
    RootProviderCreate,
    RootChangeMaxSpotLimit,
    RootUpsertSubscription
)

router = APIRouter(prefix="/root", tags=["Root"])


@router.post("/new_provider")
async def create_new_provider(
        provider_data: RootProviderCreate = Body(...),
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> ProviderData:
    provider = await get_or_create_provider(session, provider_data)
    return await ProviderData.by_model(session, provider)


@router.post(
    "/change_max_spots",
    responses={
        **ProviderDoesntExist.responses,
        **ImpossibleChange.responses
    }
)
async def change_max_spots(
        data: RootChangeMaxSpotLimit,
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> ProviderData:
    provider = await change_provider_spot_limit(session, data)
    return await ProviderData.by_model(session, provider)


@router.post(
    "/subscription/upsert",
    responses={
        **SpotDoesntExist.responses
    }
)
async def upsert_subscription(
        data: RootUpsertSubscription,
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> SpotData:
    spot = await upsert_subscription_by_data(session, data)
    return await SpotData.by_model(session, spot)
