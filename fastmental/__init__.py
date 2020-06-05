from fastapi import FastAPI
from fastmental.routers import main, messenger


def create_app():
    """
    Create the app instance
    """
    app = FastAPI()
    app.include_router(main.router)
    app.include_router(messenger.router)
    return app
    