import logging
import os

def setup_logger(level=logging.INFO, log_file="logs/tool.log"):
    logger = logging.getLogger("ReconTool")
    logger.setLevel(level)

    # Prevent adding handlers multiple times in case of multiple calls
    if not logger.handlers:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

        # File handler
        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)  # Always log everything in file
        fh_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger
