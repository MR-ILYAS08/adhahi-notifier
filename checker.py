import time
import threading
import requests

from config   import API_URL, CHECK_INTERVAL, WILAYAS
from database import get_subscribers_for_wilaya, mark_notified
from emailer  import send_email
from logger   import log


def fetch_availability() -> dict[str, bool]:
    """Returns {wilaya_code: available} or empty dict on failure."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Accept":     "application/json",
        "Referer":    "https://adhahi.dz/",
    }
    try:
        r = requests.get(API_URL, headers=headers, timeout=10)
        r.raise_for_status()
        return {w["wilayaCode"]: w["available"] for w in r.json()}
    except Exception as e:
        log.warning(f"API request failed: {e}")
        return {}


def _checker_loop():
    log.info("Background checker started")
    while True:
        availability = fetch_availability()

        for code, is_available in availability.items():
            log.info("checking for %s %s", code, is_available)
            if is_available:
                subscribers = get_subscribers_for_wilaya(code)
                if subscribers:
                    wilaya_name = next(
                        (w["wilayaNameFr"] for w in WILAYAS if w["wilayaCode"] == code),
                        code
                    )
                    log.info(f"{wilaya_name} available — notifying {len(subscribers)} subscriber(s)")
                    for email in subscribers:
                        log.info("Send email to : %s %s", email, code)
                        send_email(email, wilaya_name)
                        time.sleep(3)
                    mark_notified(code)

        time.sleep(CHECK_INTERVAL)


def start_checker():
    t = threading.Thread(target=_checker_loop, daemon=True)
    t.start()


if __name__ == "__main__":
    from database import init_db
    init_db()
    log.info("Running checker standalone")
    _checker_loop()
