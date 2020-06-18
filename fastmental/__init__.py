def create_app():
    """
    Create the app instance
    """
    from fastapi import FastAPI
    from fastmental.routers import main, messenger
    app = FastAPI()
    app.include_router(main.router)
    app.include_router(messenger.router)
    return app
    