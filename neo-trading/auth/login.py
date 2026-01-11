import time
import logging
from neo_api_client import NeoAPI

logger = logging.getLogger("LOGIN")

def login_with_retry(
    consumer_key,
    mobile,
    ucc,
    mpin,
    max_attempts=None,
    sleep_between=2
):
    client = NeoAPI(
        environment="prod",
        access_token=None,
        neo_fin_key=None,
        consumer_key=consumer_key
    )

    attempt = 0

    while True:
        attempt += 1
        totp = input("Enter TOTP: ").strip()

        try:
            logger.info(f"TOTP attempt {attempt}")

            resp = client.totp_login(
                mobile_number=mobile,
                ucc=ucc,
                totp=totp
            )

            # 🔑 KEY FIX: check response before validate
            if isinstance(resp, dict) and resp.get("error"):
                logger.warning(f"TOTP invalid: {resp['error']}")
                raise ValueError("Invalid TOTP")

            # Only call validate if TOTP login succeeded
            resp2 = client.totp_validate(mpin=mpin)

            if isinstance(resp2, dict) and resp2.get("error"):
                logger.error(f"MPIN failed: {resp2['error']}")
                raise RuntimeError("MPIN validation failed")

            logger.info("Login successful")
            return client

        except Exception as e:
            logger.error(f"Login failed: {e}")

            if max_attempts and attempt >= max_attempts:
                raise RuntimeError("Max login attempts exceeded")

            time.sleep(sleep_between)
