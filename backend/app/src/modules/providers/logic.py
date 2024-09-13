__all__ = ["create_spot"]

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import Provider, Spot
from app.data.db.repositories import RepositoriesManager
from app.src.modules.providers.exceptions import MaxSpotIsReached


async def create_spot(session: AsyncSession, provider: Provider) -> Spot:
    manager = RepositoriesManager(session)

    if provider.spots + 1 > provider.max_spots:
        raise MaxSpotIsReached

    spot_service_user = await manager.U.create(Roles.spotUser)
    spot = await manager.S.create(account=spot_service_user, provider_id=provider.id)
    await manager.P.add_spot(provider, spot)
    await manager.U.set_data(spot_service_user, spot.service_user_data)
    return spot
