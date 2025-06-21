import subprocess
import logging
from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger(logging.INFO)

def detect_tech(domain):
    """
    Runs WhatWeb to detect technologies on the given domain.
    """
    try:
        logger.info(f"Executing: whatweb {domain}")
        result = subprocess.run(
            ['whatweb', '--no-errors', '--color=never', domain],
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            logger.debug(f"WhatWeb output: {output}")
            return output
        else:
            error_msg = result.stderr.strip() or "Unknown WhatWeb error."
            logger.warning(f"WhatWeb returned error: {error_msg}")
            return f"WhatWeb returned error:\n{error_msg}"
    except FileNotFoundError:
        error_msg = "WhatWeb tool not found. Ensure it is installed (e.g., sudo apt install whatweb)."
        logger.error(error_msg)
        return error_msg
    except subprocess.TimeoutExpired:
        error_msg = f"WhatWeb scan timed out for {domain}."
        logger.warning(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Technology detection failed: {e}"
        logger.error(error_msg)
        return error_msg

def run(domain):
    """
    Entry point for tech detection module.
    """
    logger.info(f"Running technology detection for {domain}...")
    result = detect_tech(domain)
    write_report(domain, result, "techdetect")
    logger.info("Technology detection completed.")
    return result
