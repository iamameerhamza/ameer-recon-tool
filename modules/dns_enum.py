import dns.resolver
import logging
import os
import sys

# Force Python to find your 'utils' folder
project_root = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(project_root, "..", "utils")
sys.path.insert(0, utils_path)

from logger import setup_logger
from report_writer import write_report

logger = setup_logger(logging.INFO)

def run(domain):
    try:
        logger.info(f"Running DNS enumeration for {domain}...")
        records = {}
        for rtype in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                records[rtype] = [rdata.to_text() for rdata in answers]
            except Exception:
                records[rtype] = []
        result = "\n".join(f"{rtype}: {records[rtype]}" for rtype in records)
        logger.info("DNS enumeration completed.")
        write_report(domain, result, "dns")
        return records
    except Exception as e:
        logger.error(f"DNS enumeration failed: {e}")
        return None
