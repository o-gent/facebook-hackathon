"""
Decision tree for selecting responses
"""

from fastmental.models.person import Person
from fastmental.response import fb_message
from typing import Dict

PEOPLE: Dict[str, Person] = {}
STATES = {
    'start': start,
    'end': start
}


def get_people():
    return PEOPLE


def handle_message(fbid:str, message):
    """
    first function to be called once a message has been recieved
    """

    person = PEOPLE.get(fbid)
    if person:
        # run the corresponding state for the person
        state = person.get_state()
        statefunc = STATES[state]
        response = statefunc(person, message)
        fb_message(int(fbid), response)

    else:
        # first message from this person
        PEOPLE[fbid] = Person(fbid)
        handle_message(fbid, message)


def start(person: Person, message):
    return "Hello!"
