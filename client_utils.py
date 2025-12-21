import os
from dotenv import load_dotenv
from neo_api_client import NeoAPI

# Load variables from .env into environment
load_dotenv()

# Access variables
consumer_key = os.getenv("consumer_key")
mobile_number = os.getenv("mobile_number")
ucc = os.getenv("ucc")
mpin = os.getenv("mpin")

class ClientSetup:
    def __init__(self):
        self.consumer_key = consumer_key
        self.mobile_number = mobile_number
        self.ucc = ucc
        self.mpin = mpin
        self.client = None
        
    def login(self, totp):
        self.client = NeoAPI(environment='prod', access_token=None, neo_fin_key=None, consumer_key=self.consumer_key)
        self.client.totp_login(mobile_number=self.mobile_number, ucc=self.ucc, totp=totp)
        self.client.totp_validate(mpin=self.mpin)
        
        # Setup Callbacks for websocket events (Optional)
        self.client.on_message = lambda message: print(message)  # called when message is received from websocket
        self.client.on_error = lambda error_message: print(error_message)  # called when any error or exception occurs in code or websocket
        self.client.on_close = lambda message: print(message)  # called when websocket connection is closed
        self.client.on_open = lambda message: print(message)  # called when websocket successfully connects

        return self.client
