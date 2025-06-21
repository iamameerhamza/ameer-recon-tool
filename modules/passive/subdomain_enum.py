import socket
import logging
import requests
import json
import re
from utils.logger import setup_logger
from utils.report_writer import write_report

requests.packages.urllib3.disable_warnings()
logger = setup_logger(logging.INFO)

def validate_domain(domain):
    pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    if re.match(pattern, domain):
        return True
    logger.error("Invalid domain format. Please enter a valid domain (e.g., example.com).")
    return False

def query_crtsh(domain):
    url = f'https://crt.sh/?q=%25.{domain}&output=json'
    logger.info(f"Querying crt.sh for {domain}")
    subdomains = set()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        for entry in data:
            name = entry.get('name_value', '')
            for sub in name.split('\n'):
                if domain in sub:
                    subdomains.add(sub.strip())
        logger.info(f"crt.sh found {len(subdomains)} unique subdomains")
    except requests.RequestException as e:
        logger.warning(f"crt.sh query failed: {e}")
    return list(subdomains)

def query_hackertarget(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    logger.info(f"Querying HackerTarget for {domain}")
    subdomains = set()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200 or "error" in response.text.lower():
            logger.warning("HackerTarget returned an error or rate limit message.")
            return []
        for line in response.text.strip().splitlines():
            parts = line.split(',')
            if parts and domain in parts[0]:
                subdomains.add(parts[0].strip())
        logger.info(f"HackerTarget found {len(subdomains)} subdomains")
    except requests.RequestException as e:
        logger.warning(f"HackerTarget query failed: {e}")
    return list(subdomains)

def brute_force_subdomains(domain, wordlist=None):
    if wordlist is None:
        wordlist = ["www", "mail", "ftp", "ns1", "dev", "test"]
    logger.info(f"Starting brute force on {domain} with {len(wordlist)} candidates")
    found = set()
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found.add(subdomain)
            logger.info(f"Brute: {subdomain} → {ip}")
        except socket.gaierror:
            continue
    return list(found)

def detect_wildcard(domain):
    fake_sub = f"nonexistent-{socket.gethostname()}.{domain}"
    try:
        ip = socket.gethostbyname(fake_sub)
        logger.info(f"Wildcard DNS detected → {ip}")
        return ip
    except socket.gaierror:
        return None

def dns_verify(subdomains, wildcard_ip=None):
    valid = []
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            if wildcard_ip and ip == wildcard_ip:
                logger.debug(f"Skipping {sub} (wildcard match)")
                continue
            valid.append(f"{sub} → {ip}")
        except socket.gaierror:
            continue
    logger.info(f"{len(valid)} subdomains passed DNS verification")
    return valid

def run(domain, wordlist_file=None):
    if not validate_domain(domain):
        return []

    wordlist = None
    if wordlist_file:
        try:
            with open(wordlist_file, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(wordlist)} entries from wordlist file")
        except Exception as e:
            logger.warning(f"Failed to load wordlist file: {e}")

    all_subs = set()
    all_subs.update(query_crtsh(domain))
    all_subs.update(query_hackertarget(domain))
    all_subs.update(brute_force_subdomains(domain, wordlist))

    wildcard_ip = detect_wildcard(domain)
    verified = dns_verify(all_subs, wildcard_ip)

    report_content = "\n".join(verified) if verified else "No subdomains found."
    write_report(domain, report_content, "subdomains")

    return verified
