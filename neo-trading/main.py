from db.connection import get_connection
from db.schema import init_schema

def main():
    conn = get_connection()
    init_schema(conn)
    print("DB ready. Plug websocket here.")

if __name__ == "__main__":
    main()
