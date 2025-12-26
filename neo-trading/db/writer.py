class TickWriter:
    def __init__(self, conn, batch_size=100):
        self.conn = conn
        self.batch_size = batch_size
        self.buffer = []

    def add(self, tick):
        self.buffer.append(tick)
        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        if not self.buffer:
            return

        self.conn.executemany("""
            INSERT INTO ticks (
                trade_date, timestamp,
                exchange, segment,
                symbol, expiry, strike, option_type,
                ltp, volume, oi, bid, ask
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                t["trade_date"],
                t["timestamp"],
                t["exchange"],
                t["segment"],
                t["symbol"],
                t.get("expiry"),
                t.get("strike"),
                t.get("option_type"),
                t.get("ltp"),
                t.get("volume"),
                t.get("oi"),
                t.get("bid"),
                t.get("ask"),
            )
            for t in self.buffer
        ])

        self.conn.commit()
        self.buffer.clear()
