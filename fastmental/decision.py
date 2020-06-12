"""
Decision tree for selecting responses
"""

from fastmental.models.person import Person

PERSON_STORE = {}
STATES = {
    'start': start,
    'end': 0
}

def handle_message(fbid:str, message):
    """
    first function to be called once a message has been recieved
    needs to return response text for that person if any
    """
    
    person = PERSON_STORE.get(fbid)
    if person:
        # run the corresponding state for the person
        state = person.get_state()
        statefunc = STATES.get(state)
        return statefunc(person, message)
    else:
        # first message from this person
        PERSON_STORE[fbid] = Person(fbid)
        return handle_message(fbid, message)


def start(person: Person, message):
    pass
