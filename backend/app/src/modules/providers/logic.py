__all__ = ["create_spot"]
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import Provider, Spot
from app.data.db.repositories import ProviderRepository, UserRepository, SpotRepository
from app.src.modules.providers.exceptions import MaxSpotIsReached

async def create_spot(session: AsyncSession, provider: Provider) -> Spot:
    provider_repo = ProviderRepository(session)
    spot_repo = SpotRepository(session)
    user_repo = UserRepository(session)

    if provider.spots + 1 > provider.max_spots:
        raise MaxSpotIsReached

    spot_service_user = await user_repo.create(Roles.spotUser)
    spot = await spot_repo.create(account=spot_service_user, provider_id=provider.id)
    await provider_repo.add_spot(provider, spot)
    return spot
