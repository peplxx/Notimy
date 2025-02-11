__all__ = ["get_or_create_provider", "change_provider_spot_limit", "upsert_subscription_by_data"]
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import Provider, Spot
from app.data.db.repositories import RepositoriesManager
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


async def get_or_create_provider(session: AsyncSession, provider_data: RootProviderCreate) -> Provider:
    """
    Retrieve an existing provider by name or create a new one if it does not exist.

    Args:
        session (AsyncSession): The database session to use for the operation.
        provider_data (RootProviderCreate): Data required to create a new provider.

    Returns:
        Provider: The existing provider if found, or the newly created provider.

    Raises:
        Exception: Raises an exception if the provider cannot be created due to a database error.
    """
    manager = RepositoriesManager(session)

    if result := await manager.P.get_by_name(provider_data.name):
        return result

    service_user = await manager.U.create(Roles.providerUser)

    provider = await manager.P.create(
        name=provider_data.name,
        description=provider_data.description,
        account_id=service_user.id,
    )

    await manager.U.set_data(service_user, provider.service_user_data)
    return provider


async def change_provider_spot_limit(session: AsyncSession, data: RootChangeMaxSpotLimit) -> Provider:
    """
    Change the maximum spot limit of a provider if the new limit is valid.

    Args:
        session (AsyncSession): The database session to use for the operation.
        data (RootChangeMaxSpotLimit): Data containing provider ID and the new limit value.

    Returns:
        Provider: The updated provider with the new spot limit.

    Raises:
        ProviderDoesntExist: If the provider with the specified ID does not exist.
        ImpossibleChange: If the new limit would result in an invalid state (e.g., less than current spots).
    """
    manager = RepositoriesManager(session)

    provider: Provider = await Provider.find_by_id(session, data.id)
    if not provider:
        raise ProviderDoesntExist

    if provider.max_spots + data.value < provider.spots:
        raise ImpossibleChange

    await manager.P.change_spot_limit(provider, data.value)
    return provider


async def upsert_subscription_by_data(session: AsyncSession, data: RootUpsertSubscription) -> Spot:
    """
    Upsert a subscription for a spot and update its subscription end date.

    Args:
        session (AsyncSession): The database session to use for the operation.
        data (RootUpsertSubscription): Data containing spot ID and subscription details.

    Returns:
        Spot: The spot with the updated subscription details.

    Raises:
        SpotDoesntExist: If the spot with the specified ID does not exist.
    """
    manager = RepositoriesManager(session)

    spot = await Spot.find_by_id(session, data.spot_id)
    if not spot:
        raise SpotDoesntExist
    subscription = await manager.S.force_subscription(spot)
    await manager.S.change_subscription_ends(subscription, timedelta(days=data.days))
    return spot
