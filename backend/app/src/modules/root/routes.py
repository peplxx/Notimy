from datetime import timedelta, datetime, timezone
from json import dumps

from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import Provider, User, Spot, Subscription
from app.src.common.dtos import ProviderData, SpotData
from app.src.middleware.token_auth import root_auth
from app.src.modules.root.exceptions import ProviderDoesntExist, ImpossibleChange, SpotDoesntExist
from app.src.modules.root.schemas import RootProviderCreate, RootChangeMaxSpotLimit, RootUpsertSubscription

router = APIRouter(prefix="/root", tags=["Root"])

now = datetime.now(tz=timezone.utc).replace(tzinfo=None)

@router.post("/new_provider")
async def create_new_provider(
        provider_data: RootProviderCreate = Body(...),
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
):
    existing_provider: Provider = await session.scalar(
        select(Provider).where(Provider.name == provider_data.name)
    )
    if existing_provider:
        response = (await ProviderData.by_model(session, existing_provider)).__dict__
        response.update({"type": "existing"})
        return response
    provider_service_account = User(
        role=Roles.providerUser.value
    )
    session.add(provider_service_account)
    await session.commit()

    provider = Provider(
        name=provider_data.name,
        description=provider_data.description,
        account=provider_service_account.id
    )
    session.add(provider)
    await session.commit()
    provider_service_account.set_data(
        provider.service_user_data
    )
    await session.commit()

    response = (await ProviderData.by_model(session, provider)).__dict__
    response.update({"type": "new"})
    return response


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
):
    provider: Provider = await Provider.find_by_id(session, data.id)
    if not provider:
        raise ProviderDoesntExist
    if provider.max_spots + data.value < provider.spots:
        raise ImpossibleChange
    provider.max_spots += data.value
    await session.commit()
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
):
    spot = await Spot.find_by_id(session, data.spot_id)
    if not spot:
        raise SpotDoesntExist

    subscription = await session.scalar(select(Subscription).where(
        Subscription.spot_id == spot.id
    ))

    if subscription and subscription.expires_at:
        subscription.expires_at += timedelta(days=data.days)  # Extend existing subscription
    if not subscription:
        subscription = Subscription(
            spot_id=spot.id,
            provider_id=spot.provider,
            expires_at=now + timedelta(days=data.days)
        )
        session.add(subscription)  # Create new subscription
    await session.commit()
    return await SpotData.by_model(session, spot)
