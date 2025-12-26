def init_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS ticks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_date TEXT NOT NULL,
        timestamp INTEGER NOT NULL,

        exchange TEXT NOT NULL,
        segment TEXT NOT NULL,

        symbol TEXT NOT NULL,
        expiry TEXT,
        strike INTEGER,
        option_type TEXT,

        ltp REAL,
        volume INTEGER,
        oi INTEGER,
        bid REAL,
        ask REAL
    );

    CREATE INDEX IF NOT EXISTS idx_ticks_main
    ON ticks (
        trade_date,
        symbol,
        expiry,
        strike,
        option_type,
        timestamp
    );
    """)
    conn.commit()
