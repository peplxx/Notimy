__all__ = ['SpotRepository']

from datetime import timedelta
from uuid import UUID

from sqlalchemy import select

from app.data.db.models import Spot, Subscription, User, Alias
from app.data.db.repositories.base import BaseRepository
from app.data.db.utils import get_now as now


class SpotRepository(BaseRepository):

    async def create(self, account: User, provider_id: UUID) -> Spot:
        spot = Spot(
            account=account,
            provider_id=provider_id
        )
        self._session.add(spot)
        alias = Alias(base=spot.id)
        self._session.add(alias)
        await self._session.commit()
        return spot

    async def force_subscription(self, spot: Spot) -> Subscription:
        if result := await self.get_subscription(spot):
            return result
        return await self.create_subscription(spot)

    async def get_subscription(self, spot: Spot) -> Subscription:
        return await self._session.scalar(select(Subscription).where(Subscription.spot_id.is_(spot.id)))

    async def create_subscription(self, spot: Spot) -> Subscription:
        subscription = Subscription(
            spot_id=spot.id,
            provider_id=spot.provider_id,
        )
        self._session.add(subscription)
        await self._session.commit()
        return subscription

    async def change_subscription_ends(self, spot_subscription: Subscription, delta=timedelta):
        if not spot_subscription.expires_at:  # Expiration Date is not Null
            spot_subscription.expires_at = now()
        spot_subscription.expires_at += delta
        await self._session.commit()

    async def change_alias(self, spot: Spot, alias_name) -> Alias:
        alias_db: Alias = await self._session.scalar(select(Alias).where(Alias.base.is_(spot.id)))
        alias_db.name = alias_name
        await self._session.commit()
        return alias_db

    async def get_channel_ids(self, spot: Spot) -> list[UUID]:
        return [_.id for _ in await spot.channels_list]