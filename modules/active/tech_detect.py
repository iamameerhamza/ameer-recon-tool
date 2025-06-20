import subprocess
import os
import sys


from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger()

def detect_tech(domain):
    try:
        result = subprocess.run(['whatweb', domain], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error running whatweb: {result.stderr.strip()}"
    except Exception as e:
        return f"Technology detection failed: {e}"

def run(domain):
    logger.info(f"Running technology detection for {domain}...")
    result = detect_tech(domain)
    write_report(domain, result, "techdetect")
    logger.info("Technology detection completed.")
    return result
