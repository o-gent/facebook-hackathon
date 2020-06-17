# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 21:04:33 2020

@author: denis
"""

#create a class that will move through the 
from wit import Wit

#dictionary of all wit keys, this needs to get updated
wit_key_dict = {
    'HappyOrSad': Wit('UPLNVFMXPWAJATA5YMFTGXVW27JR6EZN'),
    'ReasonForDistress' : Wit('65ZE46TD7DCBJX3KK5GZAXQSWFO3F3K7'),
    }

class Person:
    #class to define the user    
    def __init__(self):
        self.state = "start"
        self.end = 'no'
        self.ind = 'you'
        #self.text = '' # this is the text varia
        
    def welcome(self): #always run on start of new class
        print('Hello and welcome to the mental health bot!\nWe aim to help solve any issues you or a friend may have.\n Are you asking for a friend or yourself?', ['Myself','Friend'])
        return 'Hello and welcome to the mental health bot!\nWe aim to help solve any issues you or a friend may have.\n Are you asking for a friend or yourself?', ['Myself','Friend']
        
    
    def run_step(self,text:str):
        if self.state == 'start':
            self.how_are_you(text)
        elif self.state == 'HappyOrSad':
            self.happy_or_sad(text)
        elif self.state == 'ReasonForDistress':
            self.identify_reason(text)

            
    def how_are_you(self,text):
        self.state = 'HappyOrSad'
        if text == 'Myself':
            self.ind = 'you'
            # return 'How are you doing today?'
        else:
            self.ind = 'they'
        return f'How are {self.ind} doing today?'
        
        
        
        #print('We from the team hope this helps, please come talk to us again if you want to!')
    #to be run at any point that the bot reaches the end    
    def end(self):
        self.state = "start"
        self.end = 'no'
        self.ind = 'you'
        return('We from the team hope this helps, please come talk to us again if you want to!')
        

        
    def happy_or_sad(self,text:str):
        client = wit_key_dict[self.state]
        resp = client.get_message(text) # would actually need to be an input  
        self.answer = resp['outcomes'][0]['entities']['intent'][0]['value']
        if self.answer == 'Happy':
            self.state='end'
            return(f'We are glad {self.ind} are feeling good! Please come back if {self.ind} ever want help with something :)')
            
        else:
            self.state = 'ReasonForDistress'
  
            return f'Oh no, I am sorry to hear that!\nCould {self.ind} tell me a bit more about what is bringing you down?\n'
       
        
    def identify_reason(self,text):
        client = wit_key_dict[self.state]
        resp = client.get_message(text)['outcomes'][0]['entities']['intent'][0]['value']
        self.state=resp
        return f'Could {self.ind} tell me what is causing one to be {resp}'

        
                
        

denis = Person()
denis.welcome()

denis.run_step('Friend')
print(denis.ind)
print(denis.state)
# denis.test_question_loop()