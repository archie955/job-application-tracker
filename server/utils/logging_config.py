import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename="log.log",
        filemode="w",
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )