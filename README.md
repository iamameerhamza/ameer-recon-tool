# AmeerReconTool 

A Python-based automated recon tool designed to gather information about a target domain using modules like WHOIS lookup, DNS enumeration, subdomain discovery, port scanning, banner grabbing, and technology detection.

---

##  Features

- WHOIS lookup
- DNS record enumeration
- Subdomain brute-forcing
- Port scanning (common ports)
- Banner grabbing (basic service info)
- Technology stack detection
- Summary report generation

---

##  Project Structure

```
.
├── main.py                  # Main controller script
├── generate_summary.py      # Compiles all module reports into one summary
├── modules/                 # Recon modules
│   ├── whois_lookup.py
│   ├── dns_enum.py
│   ├── subdomain_enum.py
│   ├── port_scan.py
│   ├── banner_grab.py
│   └── tech_detect.py
├── utils/
│   ├── logger.py            # Logging setup
│   └── report_writer.py     # Handles saving output to files
├── reports/                 # Output files from each module
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repo:
```bash
git clone https://github.com/iamameerhamza/ameer-recon-tool
cd ameer-recon-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

---

##  Usage

### Run recon on a domain:
```bash
python3 main.py --domain example.com
```

This will run all modules in sequence and save the results in the `reports/` folder.

### Generate a final summary report:
```bash
python3 generate_summary.py --domain example.com
```

This will create `final_report_example.com.txt` with all findings.

---

## Modules Description

| Module         | Description                                         |
|----------------|-----------------------------------------------------|
| WHOIS Lookup   | Fetches domain registration details                 |
| DNS Enum       | Retrieves DNS records (A, MX, NS, TXT)              |
| Subdomain Enum | Discovers subdomains using a wordlist               |
| Port Scan      | Scans for common open TCP ports                     |
| Banner Grab    | Attempts to fetch service banners (version info)    |
| Tech Detect    | Analyzes headers and HTML to detect technologies    |

---

##  Output

Each module saves its output in:
```
/reports/domainname_modulename.txt
```

Example:
- `httpbin.org_whois.txt`
- `httpbin.org_portscan.txt`
- `final_report_httpbin.org.txt`

---

## Timestamping

Each module execution includes a timestamp saved to:
```
reports/domainname_timestamp.txt
```

---

##  Tested Domains

- `httpbin.org`
- `neverssl.com`

Try others like:
```bash
python3 main.py --domain example.com
```

---

##  Notes

- Timeout errors may appear for ports that don’t respond — this is expected.
- Summary file will overwrite if you regenerate it for the same domain.

---

##  Submission

To submit:
1. Delete any unused test scripts (like `test1.py`, `test.py`)
2. Run a final clean test
3. Zip the full project:
```bash
zip -r ameer_recon_tool.zip .
```

---

Created with ❤️ by Ameer
