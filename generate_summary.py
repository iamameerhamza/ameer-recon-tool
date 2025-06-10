import os
from datetime import datetime
import argparse

def generate_summary_report(domain):
    report_dir = "reports"
    output_file = os.path.join(report_dir, f"final_report_{domain}.txt")

    # Capture summary generation time
    generated_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Optional: Simulate scan start and end time (real ones can be passed if available)
    scan_start_time = None
    scan_end_time = None

    # Look for a timestamp file if created during main recon (optional enhancement)
    timestamp_file = os.path.join(report_dir, f"{domain}_timestamp.txt")
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as tf:
            lines = tf.readlines()
            if len(lines) >= 2:
                scan_start_time = lines[0].strip()
                scan_end_time = lines[1].strip()

    header = f"Recon Summary Report for {domain}\n"
    header += f"Generated on: {generated_on}\n"
    header += "=" * 50 + "\n\n"

    if scan_start_time and scan_end_time:
        header += f"Scan started at: {scan_start_time}\n"
        header += f"Scan ended at:   {scan_end_time}\n"
        header += "-" * 50 + "\n\n"

    report_parts = []

    for file in os.listdir(report_dir):
        if domain in file and file != f"final_report_{domain}.txt" and not file.endswith("timestamp.txt"):
            section_name = file.replace(f"_{domain}.txt", "").capitalize()
            with open(os.path.join(report_dir, file), "r") as f:
                content = f.read()
                report_parts.append(f"--- {section_name} ---\n{content}\n\n")

    with open(output_file, "w") as out:
        out.write(header + "\n".join(report_parts))

    print(f"[✓] Summary report generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a summary report for a given domain.')
    parser.add_argument('--domain', required=True, help='Domain to generate the report for')
    args = parser.parse_args()

    generate_summary_report(args.domain)
