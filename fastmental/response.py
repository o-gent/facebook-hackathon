from typing import List

import requests

from fastmental.config import Config
from fastmental.logger import setup_logger

logger = setup_logger("messenger_router", "logs/messenger_router.log")


def fb_message(sender_id: int, text: str, quick_replies: List[str] = []):
    """
    Function for returning response to messenger
    :quick_replies: an optional keyword arguement
    """

    # convert the quick reply options into the correct format
    quick_reply = [{'content_type': 'text', 'title': reply} for reply in quick_replies]

    data = {
        'recipient': {'id': sender_id},
        'message': {
            'text': text,
            'quick_replies': quick_reply
            }
    }

    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + Config.FB_PAGE_TOKEN
    
    logger.info(f"sending {text} with quick replies: {quick_replies} to {sender_id}")
    
    # Send POST request to messenger
    resp = requests.post(
        'https://graph.facebook.com/me/messages?' + qs,
        json=data
    )

    logger.info(f"got response {str(resp.content)}")
