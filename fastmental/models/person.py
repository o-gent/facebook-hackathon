from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
import pathlib
import random

from wit import Wit

from fastmental.logger import setup_logger
from fastmental.response import one_time_message, fb_message


logger = setup_logger("person", "logs/person.log")

wit_keys = {
    "sentiment":        Wit('BDJ5VETFLWKYYVDDZSJVZCOMJJTY2NBO'),
    "CoarseReason":     Wit("65ZE46TD7DCBJX3KK5GZAXQSWFO3F3K7"),
    "FineReason":       Wit("SVZ7IY777CEY3FG4GOWYUO5MO3YMGR7Q"),
}

advice_location = sorted(pathlib.Path('.').glob('**/advice.json'))[0]
# advice is stored in a json file. /app/ is required for heroku
with open(advice_location) as advice_file:
    advice:dict = json.load(advice_file)


class WitNotFound(Exception):
    pass


class WitError(Exception):
    pass


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
        self.history: Dict[int, Dict[str, Tuple[str, datetime]]] = {}
        self.session: int = 0 # keeps track of how many times the user has used the bot
        logger.info(f"{fbid} object has been created")
        
    
    def run_step(self, text: str, quick_reply: bool) -> Tuple[List[str], List[str]]:
        """ accept a text input and return a response depending on persons state """
        # Add responses for states to history
        self.record(text)

        # direct to the correct function
        if self.state == "welcome":         return self.welcome()
        if self.state == "HowAreYou":       return self.how_are_you(text, quick_reply)
        if self.state == "sentiment":       return self.sentiment(text)
        if self.state == "CoarseReason":    return self.coarse_reason(text)
        if self.state == "FineReason":      return self.fine_reason(text)
        if self.state == "advice":          return self.advice(text, quick_reply)
        if self.state == "external_advice": return self.external_advice(text, quick_reply)
        if self.state == "serious":         return self.serious(text, quick_reply)
        if self.state == "end":             return self.end()
        if self.state == "rating":          return self.rating(text, quick_reply)
        
        # a function directed to a state that doesn't exist
        return ["We encountered an error!"], []
    

    def record(self, text: str):
        """ records responses for each user session """
        # we need a way of recording which route they took
        if self.history.get(self.session) != None:
            self.history[self.session][self.get_state()] = (text, datetime.now()) 
        else:
            # new session
            self.history[self.session] = {}
            self.record(text)


    def welcome(self):
        """ greeting when person starts the conversation """
        quick_reply = ['Myself','Friend']
        message = "Hello we're no problem too small! We aim to help solve any issues you or a friend may have. Are you asking for a friend or yourself?"
        self.set_state("HowAreYou")
        return [message], quick_reply


    def how_are_you(self, text: str, quick_reply: bool):
        """ Determine how they are feeling """
        
        if quick_reply:
            self.narrative = "you" if text == "Myself" else "they"
            narrative = "you" if self.narrative == "you" else "them"
            self.set_state("sentiment")
            message = f"How are {self.narrative} doing today? Is there anything bothering {narrative}"
            return [message], []
        
        # they didn't answer with a quick reply.. so stay in the same state
        message = "Could you reply with the quick reply options? Thank you!"
        return [message], ["Myself","Friend"]
        

    def sentiment(self, text:str):
        """ Determine what the issue is if they are sad """
        try:
            value, _ = self.get_wit_value(text) # either positive, neutral or negative
        except:
            message = "Ah we couldn't tell how you are feeling 😅"
            message2 = "Could you explain in another way?"
            return [message, message2], []

        if value == "positive":
            self.set_state("end")
            message = f"We are glad {self.narrative} are feeling good!" 
            message2 = f"Please come back if {self.narrative} ever want help with something :)"
            return [message, message2], []
        
        elif value == "neutral":
            message = f"Could you eleborate a bit?"
            return [message], []

        else:
            # Lets see if we can identify anything from what they've said already
            try:
                _, coarse_confidence = self.get_wit_value(text, state = "CoarseReason")
            except:
                coarse_confidence = 0

            if coarse_confidence > 0.8:
                self.set_state("CoarseReason")
                return self.coarse_reason(text)

            self.set_state("CoarseReason")
            narrative = "them" if self.narrative == "they" else "you"
            message = f"Oh no, I am sorry to hear that!"
            message2 = f"Could you tell me a bit more about what is bringing {narrative} down?"
            return [message, message2], []
    

    def coarse_reason(self, text: str):
        """ idenitfy whether the user is feeling lonely, depressed or stressed """
        try:
            _, fine_confidence = self.get_wit_value(text, state="FineReason")
            if fine_confidence > 0.8:
                self.set_state("FineReason")
                return self.fine_reason(text)
        except:
            pass
        
        try:
            value, _ = self.get_wit_value(text)
            self.set_state("FineReason")
            message = f"It seems like {self.narrative} are feeling {value.lower()}?" 
            message2 = f"Could you tell me a bit more about why {self.narrative} may feel {value.lower()}?" 
            return [message, message2], []
        except:
            # wit failed to identify a reason
            message = f"We can't tell what's up.. 😩 Could you try explaining to a different way?"
            return message, []
    

    def fine_reason(self, text: str):
        """ 
        Used to identify stress and define response 
        Wit result can be Depression, Work, Time, Irritable, Lonely, PoorFood, PoorSleep
        """
        try:
            value, _ = self.get_wit_value(text)
            advice_options: dict = advice[value]
            self.advice_options = advice_options
            self.set_state("advice")
            return self.advice(text, False)
        except:
            # we need to ask again
            message = "We didn't understand that.. 🤔 Could you explain it in a different way?"
            return [message], []


    def advice(self, text: str, quick_reply: bool):
        """ handle returning advice! """

        if text == "No 🤔" or quick_reply == False:
            advice = self.advice_options["advice"]
            self.option = random.choice(advice)
            message = self.option["advice"]
            message2 = "Would this help? we can try and suggest something else!"
            return [message, message2], ["Tell me more!", "No 🤔", "I need more help"]

        if text == "Tell me more!" and quick_reply:
            self.set_state("external_advice")
            return self.external_advice(text, quick_reply)
        
        if text == "I need more help" and quick_reply:
            self.set_state("serious")
            return self.serious(text, quick_reply)
    
        return ["Please use the quick reply options!"], ["Tell me more!", "No 🤔", "I need more help"]
    

    def external_advice(self, text: str, quick_reply: bool):
        """ just another frickin loop thing """

        if text == "Tell me more!" and quick_reply:
            external = self.option["external"]
            return [external], ["That's good!", "Something else?"]
        
        if text == "That's good!" and quick_reply:
            self.set_state("end")
            return self.end()
        
        if text == "Something else?" and quick_reply:
            self.set_state("advice")
            # start the advice loop again
            return self.advice(text, False)
        
        return ["Please use the quick reply options!"], ["That's good!", "Something else?"]


    def serious(self, text: str, quick_reply: bool):
        """ let's get down to business """
        if text == "end" and quick_reply:
            self.set_state("end")
        advice = self.advice_options["serious"].pop()
        return [advice], ["Send more", "end"]


    def end(self):
        """ 
        To be run at any point that the bot reaches the end 
        handle setup for the next run
        """
        self.set_state("rating")
        self.session += 1
        resp = one_time_message(self.fbid, "We could see how our suggestion went in a week?")
        logger.info(f"one-time request got: {resp.json()}")
        message = "The team hope this helps, please come talk to us again if you want to!"
        message2 = "Also please let us know what you throught about the conversation by leaving a rating!"
        return [message, message2], ['1', '2', '3', '4', '5']
    

    def rating(self, text: str, quick_reply: bool):
        """ rate the user experiance at the end of the conversation """
        self.set_state("welcome")
        # do something with the rating
        message = "Thank you for the rating!"
        return [message], []
    

    def handle_one_time(self, optin_token: str):
        fb_message(self.fbid, ["Great!", "we'll see how that goes in a week then"], ['1', '2', '3', '4', '5'])
    
    
    def get_wit_value(self, text: str, state = "") -> Tuple[str, float]:
        """ 
        shorcut for wit response 
        Raises:
            WitNotFound
            WitError
        """
        client = wit_keys[self.state] if state == "" else wit_keys[state]
        response = client.get_message(text)
        
        try:
            entities = response['outcomes'][0]['entities']
            get_value = lambda x: entities[x][0]['value']
            get_confidence = lambda x: entities[x][0]['confidence']

            if entities.get("sentiment"):
                value, confidence = get_value("sentiment"), get_confidence("sentiment")
                return value, confidence
            if entities.get("intent"):
                value, confidence = get_value("intent"), get_confidence("intent")
                logger.info(f"for state {state} we got {value} at {confidence}")
                return value, confidence
            # conditions weren't met, wit couldn't identify an entity
            logger.info(response)
            raise WitNotFound()

        except:
            logger.info(f"got wit response error {response}")
            raise WitError()
    

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
