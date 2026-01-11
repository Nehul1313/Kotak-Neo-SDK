import logging
from datetime import datetime
import os


def setup_logging():
    today = datetime.now().strftime("%Y-%m-%d")
    base_dir = f"logs/{today}"
    os.makedirs(base_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # Login log
    login_file = logging.FileHandler(f"{base_dir}/login.log")
    login_file.setFormatter(formatter)

    # Root logger
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    root.addHandler(console)
    root.addHandler(login_file)
