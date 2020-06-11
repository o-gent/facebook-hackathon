from typing import List, Optional

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import HTMLResponse

from fastmental.config import Config
from fastmental.models.messenger import WebhookEntry
from fastmental.response import fb_message

router = APIRouter()


@router.get("/webhook")
async def messenger_webhook(request: Request, response: Response):
    """
    A webhook to return a challenge (to check our identity)
    Messenger calls this page to check our identity
    We need to use the Request object as fb has "." in its url params
    """
    verify_token: str = request.query_params.get("hub.verify_token")
    if verify_token == Config.FB_VERIFY_TOKEN:
        challenge = request.query_params.get("hub.challenge")
        return HTMLResponse(content=challenge, status_code=200)
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return "Invalid Request or Verification Token"


@router.post("/webhook")
async def messenger_post(object: str, entries):
    """
    Handle a messenger event
    Messenger calls this page with message data when one is sent by a user
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    if object != "page":
        # as far as I can tell we are only interested in page events
        return "whaaa"
    
    for entry in entries:
        print(entry)
        print(entry.id)
        message = entry.messaging[0] # even though this is an array, it will only contain one value
        print(message.message.text)
