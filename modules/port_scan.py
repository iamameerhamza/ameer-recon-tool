# modules/port_scan.py

import socket
import logging
import os
import sys

# Set up utils path
project_root = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(project_root, "..", "utils")
sys.path.insert(0, utils_path)

from logger import setup_logger
from report_writer import write_report

logger = setup_logger(logging.INFO)

def run(target, ports=None):
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]

    logger.info(f"Starting port scan for {target}...")

    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                logger.info(f"Port {port} is OPEN")
                open_ports.append(port)
            sock.close()
        except Exception as e:
            logger.warning(f"Error checking port {port}: {e}")

    if open_ports:
        report = "\n".join([f"Port {p} is OPEN" for p in open_ports])
    else:
        report = "No open ports found."

    write_report(target, report, "portscan")
    logger.info("Port scan completed.")
    return open_ports
