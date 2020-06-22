from typing import List
import random
import time

import requests

from fastmental.config import Config
from fastmental.logger import setup_logger

logger = setup_logger("messenger_router", "logs/messenger_router.log")


def fb_message(sender_id: int, text: List[str], quick_replies: List[str]):
    """
    Function for returning response to messenger
    """

    idx=0
    while idx<len(text):
        time.sleep(random.random())
        msgText=text[idx]

        data: dict = {
            'recipient': {'id': sender_id},
            'message': {
                'text': msgText
            }
        }

        # convert the quick reply options into the correct format and add to the payload
        if quick_replies != []:
            # payload is set to the same as the title, but these could be different
            quick_reply = [{'content_type': 'text', 'title': reply, 'payload': reply} for reply in quick_replies]
            data['message']['quick_replies'] = quick_reply

        # Setup the query string with your PAGE TOKEN
        qs = 'access_token=' + Config.FB_PAGE_TOKEN

        logger.info(f"sending {msgText} with quick replies: {quick_replies} to {sender_id}")

        # Send POST request to messenger
        resp = requests.post(
            'https://graph.facebook.com/me/messages?' + qs,
            json=data
        )
        
        try:
            resp.json()['message_id']
            idx+=1
        except:
            pass

        logger.info(f"got message send response {str(resp.content)}")


def one_time_message(sender_id: int, title: str):
    """
    One time reply function 
    https://developers.facebook.com/docs/messenger-platform/send-messages/one-time-notification
    """

    data: dict = {
        "recipient": {
            "id":sender_id
        },
        "message": {
            "attachment": {
            "type":"template",
            "payload": {
                "template_type":"one_time_notif_req",
                "title":title,
                "payload":"one-time"
                }
            }
        }
    }

    qs = 'access_token=' + Config.FB_PAGE_TOKEN

    logger.info(f"sending one-time notification request with {title} to {sender_id}")

    resp = requests.post(
        'https://graph.facebook.com/me/messages?' + qs,
        json=data
    )

    return resp
