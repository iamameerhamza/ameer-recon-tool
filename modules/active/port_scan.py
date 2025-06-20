import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logger import setup_logger
from utils.report_writer import write_report

logger = setup_logger(logging.INFO)

def scan_port(target_ip, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                logger.info(f"Port {port} is OPEN")
                return port
    except Exception as e:
        logger.warning(f"Error scanning port {port}: {e}")
    return None

def run(target, ports=None, max_workers=500):
    logger.info(f"Starting threaded port scan for {target}...")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        logger.error(f"Unable to resolve {target}.")
        return []

    if ports is None:
        ports = range(1, 1025)  # You can change to 1-65536 for full scan

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port): port for port in ports}
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
            except Exception as e:
                logger.warning(f"Thread error for port {port}: {e}")

    if open_ports:
        report = "\n".join([f"Port {p} is OPEN" for p in sorted(open_ports)])
    else:
        report = "No open ports found."

    write_report(target, report, "portscan")
    logger.info("Threaded port scan completed.")
    return open_ports
