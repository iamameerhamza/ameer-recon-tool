import dns.resolver
import logging
from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger(logging.INFO)

def run(domain):
    """
    Perform DNS enumeration for the target domain.
    Queries for A, AAAA, MX, NS, and TXT records.
    Returns a dictionary of record types and their values.
    """
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']

    logger.info(f"Starting DNS enumeration for: {domain}")

    try:
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype, lifetime=5.0)
                records[rtype] = [rdata.to_text() for rdata in answers]
                logger.info(f"{rtype} records: {records[rtype]}")
            except dns.resolver.NoAnswer:
                logger.warning(f"No {rtype} records found for {domain}.")
                records[rtype] = []
            except dns.resolver.NXDOMAIN:
                logger.error(f"Domain {domain} does not exist. Aborting DNS enumeration.")
                return None
            except dns.exception.Timeout:
                logger.warning(f"Timeout while querying {rtype} records for {domain}.")
                records[rtype] = []
            except Exception as e:
                logger.error(f"Error querying {rtype} records for {domain}: {e}")
                records[rtype] = []

        # Prepare report content
        report_lines = []
        for rtype in record_types:
            report_lines.append(f"{rtype} records:")
            report_lines.extend(records[rtype] if records[rtype] else ["None"])
            report_lines.append("")  # Blank line between record types

        report_content = "\n".join(report_lines)
        write_report(domain, report_content, "dns")

        logger.info("DNS enumeration completed successfully.")
        return records

    except Exception as e:
        logger.error(f"Critical DNS enumeration failure: {e}")
        return None
