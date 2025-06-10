import socket
import logging
import os
import sys

# Setup path to utils
project_root = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(project_root, "..", "utils")
sys.path.insert(0, utils_path)

from logger import setup_logger
from report_writer import write_report

logger = setup_logger(logging.INFO)

def run(target, ports=None):
    if ports is None:
        ports = [21, 22, 23, 25, 80, 110, 143, 443, 3306, 8080]

    logger.info(f"Starting banner grabbing for {target}...")

    banners = []

    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((target, port))

            if port in [80, 8080, 443]:
                try:
                    s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if banner:
                        banners.append(f"Port {port}: {banner}")
                        logger.info(f"[+] {port} >> {banner}")
                    else:
                        banners.append(f"Port {port}: No banner received (HTTP)")
                except Exception as e:
                    banners.append(f"Port {port}: No response/broken HTTP banner")
                    logger.warning(f"[HTTP Error] Port {port}: {e}")
            else:
                try:
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if banner:
                        banners.append(f"Port {port}: {banner}")
                        logger.info(f"[+] {port} >> {banner}")
                    else:
                        banners.append(f"Port {port}: No banner received")
                except Exception as e:
                    banners.append(f"Port {port}: No response/broken banner")
                    logger.warning(f"[Banner Error] Port {port}: {e}")

            s.close()
        except Exception as e:
            logger.warning(f"Could not connect to port {port}: {e}")

    result = "\n".join(banners)
    write_report(target, result, "bannergrab")
    logger.info("Banner grabbing completed.")
    return banners
