import whois
import logging
import os
import sys

from utils.logger import setup_logger
from utils.report_writer import write_report

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
