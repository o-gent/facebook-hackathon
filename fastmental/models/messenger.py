from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    """
    Message content
    """
    mid: str
    text: str
    quick_reply: dict


class Read(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/message-reads
    """
    watermark: int


class Messages(BaseModel):
    """
    Mid-level model for "messages" events, meta data about message
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages
    """
    sender: dict # contains {"id": ".."}
    recipient: dict # contains {"id": ".."}
    timestamp: int
    message: Optional[Message]
    read: Optional[Read]


class WebhookEntry(BaseModel):
    """
    top level model for webhook events
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    id: str
    time: int
    messaging: List[Messages] # even though this is an array, it will only contain one value
