from datetime import datetime
from typing import Dict, Optional, List


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

    def handle_message(self, text: str):
        """
        
        """
        # add to the history
        
        return
    
    def handle_read(self):
        pass

    def get_state(self):
        return self._state
