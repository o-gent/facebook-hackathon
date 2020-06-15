# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 21:04:33 2020

@author: denis
"""

#create a class that will move through the 
from wit import Wit

#dictionary of all wit keys
wit_key_dict = {
    'HappyOrSad': Wit('UPLNVFMXPWAJATA5YMFTGXVW27JR6EZN'),
    'ReasonForDistress' : Wit('65ZE46TD7DCBJX3KK5GZAXQSWFO3F3K7'),
    }

class Person:
    #class to define the user    
    def __init__(self):
        self.state = "HappyOrSad"
        self.end = 'no'

        
    def run_step(self):
        func_dict = {
            'HappyOrSad':self.happy_or_sad(),
            'ReasonForDistress':self.identify_reason(),
            }
        if self.state != 'End':
            func_dict[self.state]
        else:
            self.state = 'End'
        
    def test_question_loop(self): #this loop allows for testing of the conversation internally
        while self.state != 'End':
            self.run_step()
        else:
            print('We from the team hope this helps, please come talk to us again if you want to!')
        
    def happy_or_sad(self):
        text = input('Hello, we are the mental health bot!\nPlease let me know how you are doing today?\n')
        client = wit_key_dict[self.state]
        resp = client.get_message(text) # would actually need to be an input  
        self.answer = resp['outcomes'][0]['entities']['intent'][0]['value']
        if self.answer == 'Happy':
            self.state = 'End'
        else:
            self.state = 'ReasonForDistress'
        print(f'AI response: {self.answer}') #test to see what state person is currently being assessed as
        
    def identify_reason(self):
        text = input('Oh no, I am sorry to hear that!\nCould you tell me a bit more about what is bringing you down?\n')
        client = wit_key_dict[self.state]
        resp = client.get_message(text)['outcomes'][0]['entities']['intent'][0]['value']
        print(f'AI response {resp}') #for test purposes
        self.state = 'End'
        
                
        

denis = Person()
denis.test_question_loop()
