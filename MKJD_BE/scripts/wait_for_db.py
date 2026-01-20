import argparse
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def wait_for_db(url: str, timeout: int, interval: float) -> bool:
    start = time.time()
    engine = create_engine(url, pool_pre_ping=True)
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except OperationalError:
            if time.time() - start >= timeout:
                return False
            time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wait until database is ready")
    parser.add_argument("--url", required=True, help="Database URL")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--interval", type=float, default=1.0, help="Retry interval in seconds")
    args = parser.parse_args()

    if not wait_for_db(args.url, args.timeout, args.interval):
        raise SystemExit("Database is not ready")


if __name__ == "__main__":
    main()
