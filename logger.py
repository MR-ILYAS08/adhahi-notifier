import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "adhahi.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()  # also print to terminal
    ]
)

log = logging.getLogger("adhahi")
