from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    """
    Message content
    """
    mid: str
    text: str
    quick_reply: dict


class Messages(BaseModel):
    """
    Mid-level model for "messages" events, meta data about message
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages
    """
    sender: dict # contains {"id": ".."}
    recipient: dict # contains {"id": ".."}
    timestamp: int
    message: Message


class WebhookEntry(BaseModel):
    """
    top level model for webhook events
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    id: str
    time: int
    messaging: List[Messages]