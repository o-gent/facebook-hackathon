import requests
from fastmental.config import Config
from fastmental.logger import setup_logger


logger = setup_logger("messenger_router", "logs/messenger_router.log")


def fb_message(sender_id: int, text: str):
    """
    Function for returning response to messenger
    """

    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }

    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + Config.FB_PAGE_TOKEN
    
    logger.info(f"sending {text} to {sender_id}")
    
    # Send POST request to messenger
    resp = requests.post(
        'https://graph.facebook.com/me/messages?' + qs,
        json=data
    )

    logger.info(f"got response {str(resp.content)}")
