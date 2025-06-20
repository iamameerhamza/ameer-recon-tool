import sys
import os
import argparse
import logging
from datetime import datetime
import socket
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import your tool modules
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
    args = parser.parse_args()
    domain = args.domain
    verbose = args.verbose

    logger = setup_logger(logging.DEBUG if verbose else logging.INFO)

    try:
        target_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        logger.error(f"Unable to resolve domain {domain}. Exiting.")
        print(f"{Fore.RED}[✗] Unable to resolve domain {domain}. Exiting.")
        return

    os.makedirs("reports", exist_ok=True)

    start_time = datetime.now()
    print(f"\n{Fore.CYAN}========== AMEER RECON TOOL ==========")
    print(f"{Fore.GREEN}[+] Target: {domain} ({target_ip})")
    print(f"{Fore.GREEN}[+] Scan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # WHOIS
    print(f"{Fore.YELLOW}------ WHOIS Lookup ------")
    whois_data = whois_run(domain)
    if verbose:
        print(str(whois_data)[:500] + "..." if whois_data else f"{Fore.RED}No WHOIS data.")
    write_report(domain, str(whois_data), "whois")

    # DNS
    print(f"\n{Fore.YELLOW}------ DNS Records ------")
    dns_data = dns_run(domain)
    if dns_data:
        for k, v in dns_data.items():
            print(f"{Fore.CYAN}{k}{Style.RESET_ALL}: {', '.join(v)}")
    else:
        print(f"{Fore.RED}No DNS records found.")
    write_report(domain, str(dns_data), "dns")

    # Subdomains
    print(f"\n{Fore.YELLOW}------ Subdomain Enumeration ------")
    subdomains = subdomain_run(domain)
    if subdomains:
        print(f"{Fore.GREEN}Found {len(subdomains)} subdomains:")
        if verbose:
            for s in subdomains:
                print(f"- {s}")
    else:
        print(f"{Fore.RED}No subdomains found.")
    write_report(domain, "\n".join(subdomains), "subdomains")

    # Port Scan
    print(f"\n{Fore.YELLOW}------ Port Scan ------")
    open_ports = portscan_run(target_ip)
    if open_ports:
        for p in open_ports:
            print(f"{Fore.GREEN}Port {p} is OPEN")
    else:
        print(f"{Fore.RED}No open ports found.")
    write_report(domain, "\n".join(f"Port {p} is OPEN" for p in open_ports), "portscan")

    # Banner Grabbing
    print(f"\n{Fore.YELLOW}------ Banner Grabbing ------")
    banners = banner_run(target_ip, open_ports)
    if banners:
        for p, b in banners.items():
            print(f"{Fore.CYAN}Port {p}: {b}")
    else:
        print(f"{Fore.RED}No banners retrieved.")
    write_report(domain, "\n".join(f"Port {p}: {b}" for p, b in banners.items()), "banner")

    # Technology Detection
    print(f"\n{Fore.YELLOW}------ Technology Detection ------")
    tech = tech_run(domain)
    if tech:
        if verbose:
            print(tech)
        else:
            print(f"{Fore.GREEN}Technologies detected.")
    else:
        print(f"{Fore.RED}No technologies detected.")
    write_report(domain, tech, "tech")

    # HTML report
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

    # Summary
    print(f"\n{Fore.CYAN}========== SCAN SUMMARY ==========")
    print(f"{Fore.GREEN}[✓] Recon completed for {domain}")
    print(f"{Fore.GREEN}[✓] Reports saved in 'reports/' directory")
    print(f"{Fore.GREEN}[✓] Timestamps: {start_time.strftime('%Y-%m-%d %H:%M:%S')} → {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    main()
