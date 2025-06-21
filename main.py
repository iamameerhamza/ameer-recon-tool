import sys
import os
import argparse
import logging
from datetime import datetime
import socket
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

from utils.logger import setup_logger
from modules.passive.whois_lookup import run as whois_run
from modules.passive.dns_enum import run as dns_run
from modules.passive.subdomain_enum import run as subdomain_run
from modules.active.port_scan import run as portscan_run
from modules.active.banner_grab import run as banner_run
from modules.active.tech_detect import run as tech_run
from utils.report_writer import write_report
from utils.html_report_writer import write_html_report

def main():
    parser = argparse.ArgumentParser(description="Ameer Recon Tool")
    parser.add_argument('--domain', required=True, help='Domain to scan')
    parser.add_argument('--verbose', action='store_true', help='Enable detailed output')
    parser.add_argument('--no-html', action='store_true', help='Skip HTML report generation')

    # Individual module flags
    parser.add_argument('--whois', action='store_true', help='Run WHOIS lookup')
    parser.add_argument('--dns', action='store_true', help='Run DNS enumeration')
    parser.add_argument('--subdomains', action='store_true', help='Run subdomain enumeration')
    parser.add_argument('--portscan', action='store_true', help='Run port scan')
    parser.add_argument('--banner', action='store_true', help='Run banner grabbing')
    parser.add_argument('--tech', action='store_true', help='Run technology detection')

    args = parser.parse_args()
    domain = args.domain
    verbose = args.verbose
    skip_html = args.no_html

    logger = setup_logger(logging.DEBUG if verbose else logging.INFO)

    try:
        target_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        logger.error(f"Unable to resolve domain {domain}. Exiting.")
        print(f"{Fore.RED}[✗] Unable to resolve domain {domain}. Exiting.")
        sys.exit(1)

    os.makedirs("reports", exist_ok=True)

    start_time = datetime.now()
    print(f"\n{Fore.CYAN}========== AMEER RECON TOOL ==========")
    print(f"{Fore.GREEN}[+] Target: {domain} ({target_ip})")
    print(f"{Fore.GREEN}[+] Scan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # If no module flags given, run everything
    run_all = not any([args.whois, args.dns, args.subdomains, args.portscan, args.banner, args.tech])

    whois_data = dns_data = subdomains = open_ports = banners = tech = None

    try:
        if args.whois or run_all:
            print(f"{Fore.YELLOW}------ WHOIS Lookup ------")
            whois_data = whois_run(domain)
            if verbose and whois_data:
                print(str(whois_data)[:500] + "...")
            elif not whois_data:
                print(f"{Fore.RED}No WHOIS data.")
            write_report(domain, str(whois_data or "No WHOIS data found"), "whois")

        if args.dns or run_all:
            print(f"\n{Fore.YELLOW}------ DNS Records ------")
            dns_data = dns_run(domain)
            if dns_data:
                for k, v in dns_data.items():
                    print(f"{Fore.CYAN}{k}{Style.RESET_ALL}: {', '.join(v) if v else 'None'}")
            else:
                print(f"{Fore.RED}No DNS records found.")
            write_report(domain, str(dns_data or "No DNS data found"), "dns")

        if args.subdomains or run_all:
            print(f"\n{Fore.YELLOW}------ Subdomain Enumeration ------")
            subdomains = subdomain_run(domain)
            if subdomains:
                print(f"{Fore.GREEN}Found {len(subdomains)} subdomains.")
                if verbose:
                    for s in subdomains:
                        print(f"- {s}")
            else:
                print(f"{Fore.RED}No subdomains found.")
            write_report(domain, "\n".join(subdomains) if subdomains else "No subdomains found", "subdomains")

        if args.portscan or run_all:
            print(f"\n{Fore.YELLOW}------ Port Scan ------")
            open_ports = portscan_run(target_ip)
            if open_ports:
                for p in open_ports:
                    print(f"{Fore.GREEN}Port {p} is OPEN")
            else:
                print(f"{Fore.RED}No open ports found.")
            write_report(domain, "\n".join(f"Port {p} is OPEN" for p in open_ports) if open_ports else "No open ports", "portscan")

        if args.banner or run_all:
            print(f"\n{Fore.YELLOW}------ Banner Grabbing ------")
            banners = banner_run(target_ip, open_ports or [])
            if banners:
                for p, b in banners.items():
                    print(f"{Fore.CYAN}Port {p}: {b}")
            else:
                print(f"{Fore.RED}No banners retrieved.")
            write_report(domain, "\n".join(f"Port {p}: {b}" for p, b in banners.items()) if banners else "No banners retrieved", "banner")

        if args.tech or run_all:
            print(f"\n{Fore.YELLOW}------ Technology Detection ------")
            tech = tech_run(domain)
            if tech:
                print(f"{Fore.GREEN}Technologies detected.")
                if verbose:
                    print(tech)
            else:
                print(f"{Fore.RED}No technologies detected.")
            write_report(domain, tech or "No technologies detected", "tech")

        # HTML report
        if not skip_html:
            data_dict = {
                "WHOIS": whois_data,
                "DNS": dns_data,
                "Subdomains": subdomains,
                "Port Scan": open_ports,
                "Banner Grab": banners,
                "Tech Detection": tech
            }
            write_html_report(domain, data_dict)

        # Timestamp
        end_time = datetime.now()
        timestamp_file = os.path.join("reports", f"{domain}_timestamp.txt")
        with open(timestamp_file, "w") as tf:
            tf.write(f"Scan started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            tf.write(f"Scan ended:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        logger.info(f"Timestamps saved at {timestamp_file}")

        print(f"\n{Fore.CYAN}========== SCAN SUMMARY ==========")
        print(f"{Fore.GREEN}[✓] Recon completed for {domain}")
        print(f"{Fore.GREEN}[✓] Reports saved in 'reports/' directory")
        print(f"{Fore.GREEN}[✓] Timestamps: {start_time.strftime('%Y-%m-%d %H:%M:%S')} → {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"{Fore.RED}[✗] An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
