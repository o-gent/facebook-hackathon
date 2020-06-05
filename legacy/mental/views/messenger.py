from flask import request

from mental.config import Config

def get_messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.args.get("hub.verify_token", "")
    # check if verify tokens match
    if verify_token == Config.FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.args.get("hub.challenge")
        return challenge
    else:
        return "Invalid Request or Verification Token"
