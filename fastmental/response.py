import requests
from fastmental.config import Config


def fb_message(sender_id: int, text: str) -> bytes:
    """
    Function for returning response to messenger
    """

    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }

    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + Config.FB_PAGE_TOKEN
    
    # Send POST request to messenger
    resp = requests.post(
        'https://graph.facebook.com/me/messages?' + qs,
        json=data
    )
    
    return resp.content
