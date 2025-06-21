import whois
import logging
from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger(logging.INFO)

def run(domain):
    """
    Perform WHOIS lookup for the given domain.
    Returns WHOIS data as string or None on failure.
    """
    try:
        logger.info(f"Running WHOIS lookup for {domain}...")

        # Perform the WHOIS query
        w = whois.whois(domain)

        if not w:
            logger.warning(f"WHOIS returned no data for {domain}")
            return None

        result = str(w)

        # Save report
        write_report(domain, result, "whois")

        logger.info("WHOIS lookup completed successfully.")
        return result

    except whois.parser.PywhoisError as e:
        logger.warning(f"No WHOIS data found for {domain}: {e}")
        return None
    except Exception as e:
        logger.error(f"WHOIS lookup failed for {domain}: {e}")
        return None
