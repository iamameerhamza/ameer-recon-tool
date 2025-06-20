import dns.resolver
import logging
from utils.logger import setup_logger
from utils.report_writer import write_report

# Setup logger
logger = setup_logger(logging.INFO)

def run(domain):
    """
    Perform DNS enumeration on the given domain.
    Queries for A, AAAA, MX, NS, and TXT records.
    """
    try:
        logger.info(f"Starting DNS enumeration for: {domain}")
        records = {}

        # List of record types to query
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']

        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype, lifetime=5.0)
                records[rtype] = [rdata.to_text() for rdata in answers]
                logger.info(f"{rtype} records found: {records[rtype]}")
            except dns.resolver.NoAnswer:
                logger.warning(f"No {rtype} records found.")
                records[rtype] = []
            except dns.resolver.NXDOMAIN:
                logger.error(f"Domain {domain} does not exist.")
                return None
            except dns.exception.Timeout:
                logger.warning(f"DNS query for {rtype} records timed out.")
                records[rtype] = []
            except Exception as e:
                logger.error(f"Error querying {rtype} records: {e}")
                records[rtype] = []

        # Format result for report
        report_content = "\n".join(
            f"{rtype} records:\n" + "\n".join(records[rtype] or ["None"])
            for rtype in record_types
        )

        write_report(domain, report_content, "dns")
        logger.info("DNS enumeration completed successfully.")

        return records

    except Exception as e:
        logger.error(f"DNS enumeration failed: {e}")
        return None
