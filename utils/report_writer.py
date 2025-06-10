from datetime import datetime

def write_report(domain, data, report_type="general"):
    filename = f"reports/{domain}_{report_type}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(filename, "w") as f:
            f.write(f"Report generated on: {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            f.write(data)
        return f"Report saved to {filename}"
    except Exception as e:
        return f"Failed to save report: {e}"
