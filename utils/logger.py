import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %I:%M:%S",
    level=logging.INFO,
)

cron_log = logging.getLogger("cron")
