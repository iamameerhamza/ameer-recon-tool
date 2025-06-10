# utils/report_writer.py

def write_report(domain, data, report_type="general"):
    filename = f"reports/{domain}_{report_type}.txt"
    try:
        with open(filename, "w") as f:
            f.write(data)
        return f"Report saved to {filename}"
    except Exception as e:
        return f"Failed to save report: {e}"
