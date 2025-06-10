import socket
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

def run(domain, wordlist=None):
    if wordlist is None:
        # a small default wordlist—feel free to expand later
        wordlist = ["www", "mail", "ftp", "ns1", "dev"]
    try:
        logger.info(f"Starting subdomain enumeration for {domain}...")
        found = []
        for sub in wordlist:
            subdomain = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(subdomain)
                logger.info(f"Found: {subdomain} → {ip}")
                found.append(f"{subdomain} → {ip}")
            except Exception:
                # silently ignore if it doesn’t resolve
                continue

        result_data = "\n".join(found) if found else "No subdomains found."
        logger.info("Subdomain enumeration completed.")
        write_report(domain, result_data, "subdomains")
        return found
    except Exception as e:
        logger.error(f"Subdomain enumeration failed: {e}")
        return None
