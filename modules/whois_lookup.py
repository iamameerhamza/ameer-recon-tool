import whois
import logging
import os
import sys

# Fix path for utils
project_root = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(project_root, "..", "utils")
sys.path.insert(0, utils_path)

from logger import setup_logger
from report_writer import write_report

logger = setup_logger(logging.INFO)

def run(domain):
    try:
        logger.info(f"Running WHOIS lookup for {domain}...")
        w = whois.whois(domain)
        result = str(w)
        logger.info("WHOIS lookup completed.")
        write_report(domain, result, "whois")
        return result
    except Exception as e:
        logger.error(f"WHOIS lookup failed: {e}")
        return None
