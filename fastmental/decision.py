"""
Decision tree for selecting responses
"""

from fastmental.models.person import Person
from fastmental.response import fb_message
from typing import Dict


PEOPLE: Dict[int, Person] = {}


def get_people():
    return PEOPLE


def handle_message(fbid:int, message:str):
    """
    first function to be called once a message has been recieved
    """

    person = PEOPLE.get(fbid)
    if person:
        # run the corresponding state for the person
        state = person.get_state()
        statefunc = STATES[state]
        response = statefunc(person, message)
        fb_message(fbid, response)

    else:
        # first message from this person
        PEOPLE[fbid] = Person(fbid)
        handle_message(fbid, message)


def handle_delivered(fbid: int):
    person = PEOPLE.get(fbid)
    if person:
        pass 


def handle_read(fbid: int):
    person = PEOPLE.get(fbid)
    if person:
        pass


def start(person: Person, message):
    return "Hello!"


STATES = {
    'start': start,
    'end': start
}
