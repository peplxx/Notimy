__all__ = ['SpotRepository']

from datetime import timedelta
from uuid import UUID

from sqlalchemy import select, Alias
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Spot, Subscription, User
from app.data.db.utils import get_now as now


class SpotRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

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
