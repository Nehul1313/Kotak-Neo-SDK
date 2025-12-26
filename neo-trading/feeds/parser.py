from time import time
from datetime import datetime


def parse_neo_message(msg):
    """
    Convert Neo websocket message → normalized tick
    (adjust keys once you see real payloads)
    """

    return {
        "trade_date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": int(time() * 1000),

        "exchange": msg.get("exch", "NSE"),
        "segment": msg.get("e", "nse_fo"),

        "symbol": msg.get("name", "NIFTY"),
        "expiry": msg.get("expDt"),
        "strike": int(float(msg["strPrc"])) if msg.get("strPrc") else None,
        "option_type": msg.get("optTp"),

        "ltp": float(msg["ltp"]) if msg.get("ltp") else None,
        "volume": int(msg["vol"]) if msg.get("vol") else None,
        "oi": int(msg["oi"]) if msg.get("oi") else None,
        "bid": None,
        "ask": None,
    }
