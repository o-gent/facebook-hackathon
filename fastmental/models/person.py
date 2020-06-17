from datetime import datetime
from typing import Dict, Optional, List, Tuple


class History:
    message: str
    send_time: datetime
    read = Optional[datetime]


class Person:
    """
    Stores information about
    - Stage in the decision tree
    - message history
    """
    
    def __init__(self, fbid: int):
        self.fbid = fbid
        self.history: List[History] = []
        self._state = "start"


    def run_step(self, text: str, quick_reply: bool) -> Tuple[str, List[str]]:
        """ accept a text input and return a response depending on persons state """
        # add to the history
        return "Hello!", ['👀', '🔥']
    

    def handle_read(self):
        pass

    
    def handle_delivered(self):
        pass


    def get_state(self):
        return self._state
