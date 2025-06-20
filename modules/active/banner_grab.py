import socket
import logging
import requests
import ssl
from requests.exceptions import RequestException

from utils.logger import setup_logger
from utils.report_writer import write_report

requests.packages.urllib3.disable_warnings()

logger = setup_logger(logging.INFO)

def grab_http_banner(ip, port, domain):
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
        logger.warning(f"HTTP/HTTPS Error on port {port}: {e}")
        return None

def grab_raw_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, port))
        try:
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner if banner else "No banner received"
        except:
            return "No banner received"
        finally:
            sock.close()
    except Exception as e:
        logger.warning(f"Port {port}: {e}")
        return None

def run(domain, open_ports):
    logger.info(f"Starting banner grabbing for {domain}...")
    results = {}
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        logger.error(f"Unable to resolve {domain}")
        return results

    for port in open_ports:
        banner = None
        if port in [80, 8080, 443]:
            banner = grab_http_banner(ip, port, domain)

        if not banner:
            banner = grab_raw_banner(ip, port)

        results[port] = banner if banner else "No banner obtained"
        logger.info(f"Port {port} banner: {results[port]}")

    # Write to report
    report_data = "\n".join([f"{port}: {results[port]}" for port in results])
    write_report(domain, report_data, "banner")

    logger.info("Banner grabbing completed.")
    return results
