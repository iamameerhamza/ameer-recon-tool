import sys
import os
import argparse
import logging
from datetime import datetime

# Setup paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, "utils"))
sys.path.insert(0, os.path.join(project_root, "modules"))

# Import utility and module functions
from logger import setup_logger
from whois_lookup import run as whois_run
from dns_enum import run as dns_run
from subdomain_enum import run as subdomain_run
from port_scan import run as portscan_run
from banner_grab import run as banner_run
from tech_detect import run as tech_run
from report_writer import write_report

def main():
    parser = argparse.ArgumentParser(description="Recon Tool")
    parser.add_argument('--domain', required=True, help='Domain to scan')
    args = parser.parse_args()
    domain = args.domain

    logger = setup_logger(logging.INFO)

    logger.info(f"Starting recon for domain: {domain}")
    print(f"\nStarting recon for domain: {domain}")

    modules = ["whois", "dns", "subdomains", "portscan", "banner", "tech"]
    print("Modules to run:", ", ".join(modules))

    # Start timestamp
    start_time = datetime.now()

    # WHOIS
    logger.info("Running WHOIS lookup...")
    whois_data = whois_run(domain)
    write_report(domain, str(whois_data), report_type="whois")
    logger.info("WHOIS lookup completed.")

    # DNS
    logger.info("Running DNS enumeration...")
    dns_data = dns_run(domain)
    write_report(domain, str(dns_data), report_type="dns")
    logger.info("DNS enumeration completed.")

    # Subdomains
    logger.info("Running subdomain enumeration...")
    subdomains = subdomain_run(domain)
    write_report(domain, "\n".join(subdomains), report_type="subdomains")
    logger.info("Subdomain enumeration completed.")

    # Port Scan
    logger.info("Running port scan...")
    open_ports = portscan_run(domain)
    write_report(domain, str(open_ports), report_type="portscan")
    logger.info("Port scan completed.")

    # Banner Grabbing
    logger.info("Running banner grabbing...")
    banners = banner_run(domain)
    write_report(domain, str(banners), report_type="banner")
    logger.info("Banner grabbing completed.")

    # Technology Detection
    logger.info("Running technology detection...")
    tech_result = tech_run(domain)
    write_report(domain, tech_result, report_type="tech")
    logger.info("Technology detection completed.")

    # End timestamp
    end_time = datetime.now()

    # Write timestamp to file
    timestamp_file = os.path.join("reports", f"{domain}_timestamp.txt")
    with open(timestamp_file, "w") as tf:
        tf.write(f"Scan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        tf.write(f"Scan ended at:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("\nRecon completed. Summary of results:")
    print(f"[✓] Timestamps saved to: {timestamp_file}")

if __name__ == "__main__":
    main()
