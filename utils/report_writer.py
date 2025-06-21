import os
from datetime import datetime

def write_report(domain, data, report_type="general", logger=None):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{domain}_{report_type}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Report generated on: {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            f.write(data)
            if not data.endswith('\n'):
                f.write('\n')
        message = f"Report saved to {filename}"
        if logger:
            logger.info(message)
        return True, filename
    except Exception as e:
        error_msg = f"Failed to save report {filename}: {e}"
        if logger:
            logger.error(error_msg)
        return False, error_msg
