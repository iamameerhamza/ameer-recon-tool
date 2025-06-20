from datetime import datetime
import os
import json  # for pretty-printing dicts

def write_html_report(domain, data_dict, output_dir="reports"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{domain}_report_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Recon Report for {domain}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; }}
            h1 {{ color: #333; }}
            .section {{ background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 0 5px #ccc; }}
            summary {{ font-weight: bold; cursor: pointer; }}
            pre {{ background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h1>Recon Report for {domain}</h1>
        <p>Generated at {timestamp}</p>
    """

    for section, content in data_dict.items():
        if isinstance(content, dict):
            content_str = json.dumps(content, indent=4)
        elif isinstance(content, list):
            if section == "Banner Grab":
                # Format banner grab cleanly
                cleaned_items = []
                for item in content:
                    cleaned_items.append(item.replace('\r', '').replace('\\r', '').replace('\\n', '\n'))
                content_str = "\n\n".join(cleaned_items)
            else:
                content_str = "\n".join(str(item) for item in content)
        else:
            content_str = str(content)

        html_content += f"""
        <details class="section">
            <summary>{section}</summary>
            <pre>{content_str}</pre>
        </details>
        """

    html_content += """
    </body>
    </html>
    """

    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html_content)

    print(f"[+] HTML report generated: {filepath}")
