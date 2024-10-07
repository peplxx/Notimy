from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import User
from app.src.common.dtos import UserData, ChannelData


class UserChannel(BaseModel):
    id: UUID
    open: bool
    code: str
    created_at: datetime

    provider_name: Optional[str] = ""
    messages_data: Optional[list[dict]] = []

    @staticmethod
    async def by_data(channel_data: ChannelData):
        result = UserChannel(
                id=channel_data.id,
                open=channel_data.open,
                code=channel_data.code,
                created_at=channel_data.created_at,
                provider_name=channel_data.provider_name,
                messages_data=[i.dict() for i in channel_data.messages_data]
            )
        return result


class UserResponse(BaseModel):
    id: UUID
    registered_at: datetime
    role: str
    tg: Optional[bool]

    channels_ids: Optional[list[UUID]] = []
    channels_data: Optional[list] = []
    
    @classmethod
    async def by_model(
            cls,
            session: AsyncSession,
            user: User
    ):
        user_data: UserData = await UserData.by_model(session, user)

        result = cls(
            id=user_data.id,
            registered_at=user_data.registered_at,
            role=user_data.role,
            channels_ids=user_data.channels_ids,
            tg=user_data.tg,
        )
        channels_data = []
        for channel_data in user_data.channels_data:
            if user.role == Roles.default.value:
                channels_data += [await UserChannel.by_data(channel_data)]
            else:
                channels_data += [channel_data]
        result.channels_data = channels_data
        return result
