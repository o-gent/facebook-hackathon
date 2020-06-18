from datetime import datetime
from typing import Dict, List, Optional, Tuple

from wit import Wit

from fastmental.logger import setup_logger


logger = setup_logger("person", "logs/person.log")
wit_key_dict = {
    'HappyOrSad': Wit('UPLNVFMXPWAJATA5YMFTGXVW27JR6EZN'),
    'IdentifyReason' : Wit('65ZE46TD7DCBJX3KK5GZAXQSWFO3F3K7'),
}


class History:
    """ format for storing message history """
    message: str
    send_time: datetime
    read = Optional[datetime]


class Person:
    """ Stores all information about a user and handles questions and answers """

    def __init__(self, fbid: int):
        self.fbid = fbid
        self.state = "welcome"
        self.narrative = "you"
        self.history: List[History] = []
        logger.info(f"{fbid} object has been created")
        
    
    def run_step(self, text: str, quick_reply: bool) -> Tuple[str, List[str]]:
        """ accept a text input and return a response depending on persons state """
        if self.state == "welcome":         return self.welcome()
        if self.state == "HowAreYou":       return self.how_are_you(text, quick_reply)
        if self.state == 'HappyOrSad':      return self.happy_or_sad(text)
        if self.state == 'IdentifyReason':  return self.identify_reason(text)
        return "We encountered an error!", []


    def welcome(self):
        """ greeting when person starts the conversation """
        quick_reply = ['Myself','Friend']
        text = "Hello and welcome to the mental health bot! We aim to help solve any issues you or a friend may have. Are you asking for a friend or yourself?"
        self.set_state("HowAreYou")
        return text, quick_reply


    def how_are_you(self, text: str, quick_reply: bool):
        """ Determine how they are feeling """
        if quick_reply:
            self.narrative = "you" if text == "Myself" else "they"
            self.set_state("HappyOrSad")
            return f"How are {self.narrative} doing today?", []
        else:
            # they didn't answer with a quick reply.. so stay in the same state
            message = f"Could you reply with the quick reply options? Thank you!"
            return message, ["Myself","Friend"]
        

    def happy_or_sad(self, text:str):
        """ Determine what the issue is if they are sad """
        response = self._get_wit_value(text)

        if response == "Happy":
            self.set_state("end")
            message = f"We are glad {self.narrative} are feeling good! Please come back if {self.narrative} ever want help with something :)"
            return message, []    
        else:
            self.set_state("IdentifyReason")
            message = f"Oh no, I am sorry to hear that! Could {self.narrative} tell me a bit more about what is bringing you down?"
            return message, []
    

    def identify_reason(self, text: str):
        """ """
        response = self._get_wit_value(text)
        self.set_state(response)
        message = f"Could {self.narrative} tell me what is causing one to be {response}" 
        return message, []
    

    def end(self):
        """ 
        To be run at any point that the bot reaches the end 
        handle setup for the next run
        """
        self.set_state("start")
        self.narrative = "you"
        return "The team hope this helps, please come talk to us again if you want to!", []
    

    def set_state(self, state: str):
        """ setter for state """
        self.state = state
        logger.info(f"{self.fbid}'s' state changed to {state}")
    
    
    def get_state(self):
        """ getter for state """
        return self.state 


    def handle_read(self):
        """ make note of read event """
        pass

    
    def handle_delivered(self):
        """ make note of delivered event """
        pass
    
    
    def _get_wit_value(self, text: str) -> str:
        """ shorcut for wit response """
        client = wit_key_dict[self.state]
        response = client.get_message(text)
        return response['outcomes'][0]['entities']['intent'][0]['value']
