from datetime import datetime
import os
import json  # for pretty-printing dicts

def write_html_report(domain, data_dict, output_dir="reports"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{domain}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(output_dir, filename)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recon Report for {domain}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; color: #212529; }}
        h1 {{ color: #007BFF; }}
        .section {{ background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 0 5px #ccc; }}
        summary {{ font-weight: bold; cursor: pointer; }}
        pre {{ background: #e9ecef; padding: 10px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
        .timestamp {{ font-size: 0.9em; color: #6c757d; }}
    </style>
</head>
<body>
    <h1>Recon Report for {domain}</h1>
    <p class="timestamp">Generated at {timestamp}</p>
"""

    for section, content in data_dict.items():
        if not content:
            content_str = "<em>No data available.</em>"
        elif isinstance(content, dict):
            content_str = f"<pre>{json.dumps(content, indent=4)}</pre>"
        elif isinstance(content, list):
            if section.lower() == "banner grab":
                cleaned_items = [item.replace('\r', '').replace('\\r', '').replace('\\n', '\n') for item in content]
                content_str = f"<pre>{'\n\n'.join(cleaned_items)}</pre>"
            else:
                content_str = f"<pre>{'\n'.join(str(item) for item in content)}</pre>"
        else:
            content_str = f"<pre>{str(content)}</pre>"

        html_content += f"""
    <details class="section" open>
        <summary>{section}</summary>
        {content_str}
    </details>
"""

    html_content += """
</body>
</html>
"""

    os.makedirs(output_dir, exist_ok=True)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] HTML report generated: {filepath}")
        return filepath
    except Exception as e:
        print(f"[✗] Failed to generate HTML report: {e}")
        return None
