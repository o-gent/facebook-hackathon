class Person:
    """
    Stores information about
    - Stage in the decision tree
    - message history
    """
    
    def __init__(self, fbid: str):
        self.fbid = fbid
        self.history = {}
        self._state = "start"

    def handle_message(self, text: str):
        """
        ?
        """
        # handle the metadata

        return
    
    def handle_read(self):
        pass

    def get_state(self):
        return self._state
