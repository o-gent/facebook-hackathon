import sys
import os

cwd = os.getcwd()
sys.path.insert(0,cwd)

from fastmental.models.person import Person

p = Person(1)
while True:
    message = input()
    quick_reply = True if input() == "1" else False
    print(p.run_step(message, quick_reply))