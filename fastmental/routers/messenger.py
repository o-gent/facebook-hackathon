from typing import List, Optional

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import HTMLResponse

from fastmental.config import Config
from fastmental.models.messenger import WebhookEntry, Messages
from fastmental.response import fb_message
import fastmental.people_handler as people_handler
from fastmental.logger import setup_logger


router = APIRouter()
logger = setup_logger("messenger_router", "logs/messenger_router.log")


@router.get("/webhook")
async def messenger_webhook(request: Request, response: Response):
    """
    A webhook to return a challenge (to check our identity)
    Messenger calls this page to check our identity
    We need to use the Request object as fb has "." in its url params
    https://developers.facebook.com/docs/messenger-platform/webhook/
    """
    verify_token: str = request.query_params.get("hub.verify_token")
    if verify_token == Config.FB_VERIFY_TOKEN:
        challenge = request.query_params.get("hub.challenge")
        return HTMLResponse(content=challenge, status_code=200)
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return "Invalid Request or Verification Token"


@router.post("/webhook")
async def messenger_post(request: Request):
    """
    Handle a messenger event
    Messenger calls this page with message data when one is sent by a user
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/
    """
    data = await request.json()

    object_name = data.get("object")
    if object_name != "page":
        # as far as I can tell we are only interested in page events
        logger.info(f"recieved non papge object { object_name }")
        return "Error"
    
    for rawentry in data.get("entry"):
        try:
            entry = WebhookEntry(**rawentry)
            item: Messages = entry.messaging[0]
            fbid:int = item.sender['id']

            # now need to handle specific message type
            if item.message:
                
                # TODO: could this be neater?
                # if the message doesn't have a quick reply payload, this will be none
                if item.message.quick_reply:
                    quick_reply = item.message.quick_reply.get("payload", "")
                else:
                    quick_reply = ""

                text = item.message.text
                
                logger.info(f"message notification from {fbid} with text: {text} and quick_response: {quick_reply}")
                people_handler.handle_message(fbid, text, quick_reply)

            elif item.delivery:
                logger.info(f"delivery notification from {fbid}")
                people_handler.handle_delivered(fbid)
            
            elif item.read:
                logger.info(f"read notification from {fbid}")
                people_handler.handle_read(fbid)
            
            return "handled or maybe not dunno"
        
        except:
            logger.critical("entry failed to be parsed")
            return "malformed data"


@router.get("/people")
async def people():
    return get_people()
