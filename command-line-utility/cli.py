from input_handler import *
from converter import *
from state import *

def run_cli():
    print("Welcome to the hex2decimal converter. Type 'help' for list of all the commands. Type 'exit' to exit.")
    while (True):
        user_input = input(">> ")
        if (len(user_input) == 0):
            continue
        else:
            handle_input(user_input)