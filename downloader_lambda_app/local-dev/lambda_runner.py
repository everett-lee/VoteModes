import logging
import os
import sys

from downloader_lambda import run

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    if len(sys.argv) == 3 and os.getenv("ENV", "") == "local-dev":
        year = int(sys.argv[1])
        month = int(sys.argv[2])

        logging.info(f"Active environment local-dev")
        logging.info(f"Running for year {year} and month {month}")
        run(year=year, month=month)

    else:
        logging.info("Provide year and month args")
