"""
Decision tree for selecting responses
"""

from fastmental.models.person import Person
from fastmental.response import fb_message
from typing import Dict


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


def handle_message(fbid:int, message:str):
    person = fetch_person(fbid)
    response = person.handle_message(message)
    fb_message(fbid, response)


def handle_delivered(fbid: int):
    person = fetch_person(fbid) 


def handle_read(fbid: int):
    person = fetch_person(fbid)
