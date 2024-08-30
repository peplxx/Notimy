from datetime import timedelta
from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import Provider, User, Spot, Subscription
from app.data.db.utils import get_now as now
from app.src.common.dtos import ProviderData, SpotData
from app.src.middleware.token_auth import root_auth
from app.src.modules.root.exceptions import (
    ProviderDoesntExist,
    ImpossibleChange,
    SpotDoesntExist
)
from app.src.modules.root.schemas import (
    RootProviderCreate,
    RootChangeMaxSpotLimit,
    RootUpsertSubscription
)

router = APIRouter(prefix="/root", tags=["Root"])


async def get_or_create_provider(session: AsyncSession, provider_data: RootProviderCreate) -> Provider:
    """Retrieve an existing provider by name or create a new one."""
    provider: Provider = await session.scalar(
        select(Provider).where(Provider.name == provider_data.name)
    )
    if provider:
        return provider

    provider_service_account = User(role=Roles.providerUser.value)
    session.add(provider_service_account)
    await session.commit()

    new_provider = Provider(
        name=provider_data.name,
        description=provider_data.description,
        account=provider_service_account.id
    )
    session.add(new_provider)
    await session.commit()

    provider_service_account.set_data(new_provider.service_user_data)
    await session.commit()

    return new_provider


@router.post("/new_provider")
async def create_new_provider(
        provider_data: RootProviderCreate = Body(...),
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> ProviderData:
    provider = await get_or_create_provider(session, provider_data)
    provider_type = "existing" if provider.id else "new"

    response = (await ProviderData.by_model(session, provider)).__dict__
    response.update({"type": provider_type})

    return response


@router.post("/change_max_spots")
async def change_max_spots(
        data: RootChangeMaxSpotLimit,
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> ProviderData:

    provider: Provider = await Provider.find_by_id(session, data.id)

    if not provider:
        raise ProviderDoesntExist
    if provider.max_spots + data.value < provider.spots:
        raise ImpossibleChange

    provider.max_spots += data.value
    await session.commit()

    return await ProviderData.by_model(session, provider)


@router.post("/subscription/upsert")
async def upsert_subscription(
        data: RootUpsertSubscription,
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
) -> SpotData:
    spot: Spot = await Spot.find_by_id(session, data.spot_id)
    if not spot:
        raise SpotDoesntExist

    subscription: Subscription = await session.scalar(
        select(Subscription).where(Subscription.spot_id == spot.id)
    )

    if subscription:
        subscription.expires_at = (
          subscription.expires_at or now()
        ) + timedelta(days=data.days)
    else:
        subscription = Subscription(
            spot_id=spot.id,
            provider_id=spot.provider_id,
            expires_at=now() + timedelta(days=data.days)
        )
        session.add(subscription)

    await session.commit()

    return await SpotData.by_model(session, spot)
