import threading

from fastapi import APIRouter

import fastmental.people_handler as people_handler
from fastmental.logger import setup_logger

router = APIRouter()
logger = setup_logger("main", "logs/main.log")


@router.get("/")
async def index():
    logger.info(threading.get_ident())
    return {"Hello": "World"}


@router.get("/people")
async def people():
    return people_handler.get_people()
