from fastapi import APIRouter, Request
from typing import Optional, List
from fastmental.models.messenger import WebhookEntry

from fastmental.config import Config

router = APIRouter()


@router.get("/webhook")
async def messenger_webhook(request: Request):
    """
    A webhook to return a challenge (to check our identity)
    Messenger calls this page to check our identity
    We need to use the Request object as fb has "." in its url params
    """
    verify_token: str = request.query_params.get("hub.verify_token")
    if verify_token == Config.FB_VERIFY_TOKEN:
        return request.query_params.get("hub.challenge")
    else:
        return "Invalid Request or Verification Token"


@router.post("/webhook")
async def messenger_post(object: str, entries: List[WebhookEntry]):
    """
    Handle a messenger event
    Messenger calls this page with message data when one is sent by a user
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    if object != "page":
        # as far as I can tell we are only interested in page events
        return "whaaa"
    
    for entry in entries:
        print(entry.id)
        for message in entry.messaging:
            print(message.message.text)
