import socket
import logging
import requests
from requests.exceptions import RequestException
from utils.logger import setup_logger
from utils.report_writer import write_report

# Disable SSL warnings for self-signed certs etc.
requests.packages.urllib3.disable_warnings()

logger = setup_logger(logging.INFO)

def grab_http_banner(ip, port, domain):
    """
    Attempts to retrieve HTTP(S) banner using requests.
    """
    try:
        if port == 443:
            url = f"https://{ip}"
        else:
            url = f"http://{ip}:{port}"
        headers = {"Host": domain}
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        server = response.headers.get("Server", "No Server Header")
        return f"{response.status_code} {server}"
    except RequestException as e:
        logger.debug(f"HTTP(S) request failed on port {port}: {e}")
        return None

def grab_raw_banner(ip, port):
    """
    Attempts to retrieve raw service banner via socket.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((ip, port))
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
                return banner if banner else "No banner received"
            except Exception:
                return "No banner received"
    except Exception as e:
        logger.debug(f"Socket connection failed on port {port}: {e}")
        return None

def run(domain, open_ports):
    """
    Performs banner grabbing on the provided open ports of the target domain.
    """
    logger.info(f"Starting banner grabbing for {domain}...")
    results = {}

    try:
        ip = socket.gethostbyname(domain)
        logger.info(f"Resolved {domain} to {ip}")
    except socket.gaierror:
        logger.error(f"Unable to resolve {domain}")
        return results

    for port in open_ports:
        banner = None

        # Prefer HTTP grabbing on web ports
        if port in [80, 443, 8080, 8443]:
            banner = grab_http_banner(ip, port, domain)

        # Fallback to raw socket banner
        if not banner:
            banner = grab_raw_banner(ip, port)

        # Store result
        results[port] = banner if banner else "No banner obtained"
        logger.info(f"Port {port} banner: {results[port]}")

    # Write to report
    report_data = "\n".join([f"Port {port}: {results[port]}" for port in sorted(results)])
    write_report(domain, report_data, "banner")

    logger.info("Banner grabbing completed.")
    return results
