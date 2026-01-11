from auth.login import login_with_retry
from ws.client import attach_ws_handlers
from db.writer import TickWriter
from db.connection import get_connection
from db.schema import init_schema
from logging_config import setup_logging

setup_logging()

#### TOTP will be prompted in console
client = login_with_retry(
    consumer_key="d4ef4c91-012f-4005-befc-d77a9e96ee6c",
    mobile="+919824984674",
    ucc="XCP0N",
    mpin="982498"
)


# 2️⃣ DB init
conn = get_connection()
init_schema(conn)
writer = TickWriter(conn)

# 3️⃣ Instruments to subscribe
instruments = [
    {"instrument_token": "486608", "exchange_segment": "mcx_fo"}
]

# 4️⃣ Attach websocket handlers
attach_ws_handlers(client, writer, instruments)

# 5️⃣ KEEP PROCESS ALIVE
import time
while True:
    time.sleep(1)
