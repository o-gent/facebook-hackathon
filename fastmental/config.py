import os

class Config:
    """
    config variables for app
    """
    SECRET_KEY = "supersekrit"
    WIT_TOKEN = "?"
    FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "")
    FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", "")