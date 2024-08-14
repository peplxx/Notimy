from json import dumps

from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import Provider, User
from app.src.common.dtos import ProviderData
from app.src.middleware.token_auth import root_auth
from app.src.modules.root.schemas import RootProviderCreate, RootChangeMaxSpotLimit

router = APIRouter(prefix="/root", tags=["Root"])


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


@router.post("/change_max_spots")
async def change_max_spots(
        data: RootChangeMaxSpotLimit,
        session: AsyncSession = Depends(get_session),
        _auth: None = Depends(root_auth)
):
    provider: Provider = await session.scalar(
        select(Provider).where(Provider.id == data.id)
    )
    if not provider:
        # TODO: Make an exception
        return {"message": "Provider doesn't exist!"}
    if provider.max_spots + data.value < provider.spots:
        return {"message": "Can't change value!"}
    provider.max_spots += data.value
    await session.commit()
    # TODO: Extend Providers Data DTO
    return await ProviderData.by_model(session, provider)
