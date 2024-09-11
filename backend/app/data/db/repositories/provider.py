__all__ = ['ProviderRepository']

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Provider, Spot


class ProviderRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_name(self, name: str) -> Provider:
        return await self._session.scalar(select(Provider).where(Provider.name.is_(name)))

    async def set_spot_limit(self, provider: Provider, spot_limit: int) -> None:
        provider.max_spot_limit = spot_limit
        await self._session.commit()

    async def change_spot_limit(self, provider: Provider, delta: int) -> None:
        await self.set_spot_limit(provider, provider.max_spots + delta)

    async def add_spot(self, provider: Provider, spot: Spot) -> None:
        provider.spots += 1
        (await provider.spots_list).append(spot)
        await self._session.commit()

    async def update(self, provider: Provider, name: str = None, description: str = None) -> Provider:
        provider.name = name if name else provider.name
        provider.description = description if description else provider.description
        await self._session.commit()
        return provider

    async def create(self, name: str, description: str, account_id: UUID) -> Provider:
        new_provider = Provider(
            name=name,
            description=description,
            account=account_id,
        )
        self._session.add(new_provider)
        await self._session.commit()
        return new_provider

    async def delete(self, provider: Provider) -> None:
        await self._session.delete(provider)
        await self._session.commit()
