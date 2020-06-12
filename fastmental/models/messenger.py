from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    """
    Message content
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages
    """
    mid: str
    text: str
    quick_reply: Optional[dict]


class Delivery(BaseModel):
    """
    Message delivery type
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/message-deliveries
    """
    mids: List[str]
    watermark: str


class Messages(BaseModel):
    """
    Mid-level model for "messages" events, meta data about message
    """
    sender: dict # contains {"id": ".."}
    recipient: dict # contains {"id": ".."}
    timestamp: int
    message: Optional[Message]
    delivery: Optional[Delivery]


class WebhookEntry(BaseModel):
    """
    top level model for webhook events
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    id: int
    time: int
    messaging: List[Messages] # even though this is an array, it will only contain one value
