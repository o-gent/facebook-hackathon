from typing import Dict

from fastmental.logger import setup_logger
from fastmental.models.person import Person
from fastmental.response import fb_message


logger = setup_logger("people_handler", "logs/people_handler.log")
PEOPLE: Dict[int, Person] = {}


def get_people():
    return PEOPLE


def fetch_person(fbid: int) -> Person:
    """
    Handles fetching correct person object from memory
    """
    person = PEOPLE.get(fbid)
    if person:
        return person
    else:
        PEOPLE[fbid] = Person(fbid)
        return fetch_person(fbid) 


def handle_message(fbid:int, message:str, quick_reply: str):
    """ accept a message from a person and respond """
    person = fetch_person(fbid)
    response = person.handle_message(message)
    fb_message(fbid, response, quick_replies=['🔥', '👀'])


def handle_delivered(fbid: int):
    """ handles delivery event with person history """
    person = fetch_person(fbid)


def handle_read(fbid: int):
    """ handles read event with person history """
    person = fetch_person(fbid)
