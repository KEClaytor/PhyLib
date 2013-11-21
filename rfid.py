# Routines for getting the RIFD of a card
# For now we don't have a reader, so just return a number
import random
from time import sleep

def get_rfid():
    # Start listening for RFID cards
    # rfid = int( raw_input() )
    # Make sure the read was valid
    # Return the id
    # Return a 6-digit id
    rfid = random.randint(0,10)
    # Allow us some time to see what's going on
    sleep(2)
    return rfid
