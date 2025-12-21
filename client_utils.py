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
latest_tick = None
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
        self.client.on_message = ClientSetup.on_message  # called when message is received from websocket
        self.client.on_error = lambda error_message: print(error_message)  # called when any error or exception occurs in code or websocket
        self.client.on_close = lambda message: print(message)  # called when websocket connection is closed
        self.client.on_open = lambda message: print(message)  # called when websocket successfully connects
        
        self.subscribe_channels()
        
        return self.client
        
    @staticmethod
    def on_message(msg):
        global latest_tick

        # Filter only real trade ticks
        data = msg.get("data", [])
        if not data: return

        d = data[0]
        if "ltp" not in d: return

        # Normalize once
        latest_tick = {
            "token": d["tk"],
            "exchange": d["e"],
            "ltp": float(d["ltp"]),
            "volume": int(d.get("v", 0)),
            "timestamp": d.get("ltt", d.get("fdtm"))
        }
        
    def subscribe_channels(self):
        # Non_index Sockets
        instrument_tokens = [
            {"instrument_token": "486608", "exchange_segment": "mcx_fo"}, #CRUDEOIL JAN 
            ]
        
        self.client.subscribe(instrument_tokens=instrument_tokens,isIndex=False,isDepth=False)

        #Index Sockets
        instrument_tokens = [
            {"instrument_token": "Nifty 50", "exchange_segment": "nse_cm"},
            ]
        
        self.client.subscribe(instrument_tokens=instrument_tokens,isIndex=True,isDepth=False)

