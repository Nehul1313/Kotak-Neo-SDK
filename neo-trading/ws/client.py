
import logging
logger = logging.getLogger("WEBSOCKET")

def attach_ws_handlers(client, writer, instruments):

    def on_open(msg):
        logger.info("WebSocket connected")
        client.subscribe(
            instrument_tokens=instruments,
            isIndex=False,
            isDepth=False
        )

    def on_message(msg):
        try:
            writer.add_from_ws(msg)
        except Exception as e:
            logger.error(e)

    def on_error(err):
        logger.error(f"WS error: {err}")

    def on_close(msg):
        logger.warning(f"WS closed: {msg}")

    client.on_open = on_open
    client.on_message = on_message
    client.on_error = on_error
    client.on_close = on_close
