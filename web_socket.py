from datetime import datetime
import pandas as pd
nifty_df = pd.read_csv("cache_storage/nifty-options.csv")

def nifty_symbol(date, strike=None, typ="CE"):
    d = datetime.strptime(date, "%d-%m-%Y") if isinstance(date, str) else date
    strike_part = "" if typ.upper() == "FUT" else f"{float(strike):.2f}"
    return f"NIFTY{d.strftime('%d%b%y').upper()}{strike_part}{typ.upper()}"

def get_nifty_option_symbol(pScripRefKey):
    return nifty_df[nifty_df["pScripRefKey"] == pScripRefKey]["pSymbol"].values[0]

# Non_index Sockets
instrument_tokens = [
    {"instrument_token": "486608", "exchange_segment": "mcx_fo"}, 
]

#Index Sockets
instrument_tokens = [
    {"instrument_token": "Nifty 50", "exchange_segment": "nse_cm"},
]