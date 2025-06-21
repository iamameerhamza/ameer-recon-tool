import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger(logging.INFO)

def scan_port(target_ip, port, timeout=0.5):
    """
    Attempts to connect to a specific port on the target IP.
    Returns the port number if open, else None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                logger.info(f"Port {port} is OPEN")
                return port
    except socket.error as e:
        logger.debug(f"Socket error on port {port}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error on port {port}: {e}")
    return None

def run(target, ports=None, max_workers=500):
    """
    Runs a threaded port scan on the given target.
    """
    logger.info(f"Starting threaded port scan for {target}...")

    try:
        target_ip = socket.gethostbyname(target)
        logger.info(f"Resolved {target} to {target_ip}")
    except socket.gaierror:
        logger.error(f"Unable to resolve {target}. Skipping port scan.")
        return []

    if ports is None:
        ports = range(1, 1025)  # Default to common ports; modify as needed

    open_ports = []
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for port in ports:
            futures.append(executor.submit(scan_port, target_ip, port))

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
            except Exception as e:
                logger.warning(f"Error retrieving future result: {e}")

    report = (
        "\n".join([f"Port {p} is OPEN" for p in sorted(open_ports)])
        if open_ports else "No open ports found."
    )

    write_report(target, report, "portscan")
    logger.info(f"Threaded port scan completed. Open ports: {open_ports}")
    return open_ports
