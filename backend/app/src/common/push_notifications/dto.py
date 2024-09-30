from typing import Optional, List

from pydantic import BaseModel, Field


class Action(BaseModel):
    action: str = Field(..., description="The action identifier for the notification")
    title: str = Field(..., description="The title of the action button")


class NotificationData(BaseModel):
    offerId: str = Field(..., description="The ID of the offer")
    userId: str = Field(..., description="The ID of the user")


class PushNotification(BaseModel):
    title: str = Field(..., description="Title of the notification")
    body: str = Field(..., description="Body text of the notification")
    icon: Optional[str] = Field(None, description="URL of the icon for the notification")
    image: Optional[str] = Field(None, description="URL of the image for the notification")
    badge: Optional[str] = Field(None, description="URL of the badge for the notification")
    vibrate: Optional[List[int]] = Field(None, description="Vibration pattern for the notification")
    tag: Optional[str] = Field(None, description="Tag for the notification")
    actions: Optional[List[Action]] = Field(None, description="List of actions associated with the notification")
    data: Optional[NotificationData] = Field(None, description="Additional data related to the notification")
    url: Optional[str] = Field(None, description="URL associated with the notification")