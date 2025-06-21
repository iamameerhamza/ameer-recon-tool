
# 📄 **AmeerReconTool**

**A modular Python reconnaissance tool for initial information gathering during penetration tests.**  
Designed for students, interns, and red teamers to practice automated recon techniques in a structured way.

---

## 🚀 **Features**

✅ **Passive Recon**
- WHOIS lookup  
- DNS enumeration (A, AAAA, MX, NS, TXT records)  
- Subdomain discovery (crt.sh, HackerTarget API, brute force + wildcard filtering)

✅ **Active Recon**
- Port scanning (multi-threaded using Python sockets)  
- Banner grabbing (HTTP headers + raw socket banners)  
- Technology detection (via WhatWeb)

✅ **Reporting**
- Individual `.txt` reports per module  
- Combined `.html` summary report per target  

✅ **Other**
- Verbose, color-coded CLI output (using `colorama`)  
- Logs saved in `logs/tool.log`  
- Flexible command-line flags for modular execution  

---

## 🛠 **Installation**

1️⃣ Clone the repository:
```bash
git clone https://github.com/yourusername/ameer-recon-tool.git
cd ameer-recon-tool
```

2️⃣ Install required dependencies:
```bash
pip install -r requirements.txt
```
➡ **Requires:** Python 3.8+

➡ For technology detection, ensure `whatweb` is installed and in your system’s PATH:
```bash
sudo apt install whatweb  # Debian/Ubuntu
```

---

## ⚡ **Usage**

Run all modules:
```bash
python3 main.py --domain example.com
```

Run selected modules:
```bash
python3 main.py --domain example.com --whois --dns --subdomains --portscan --banner --tech
```

| Flag           | Description               |
|----------------|---------------------------|
| `--domain`      | Target domain (required)   |
| `--whois`       | Run WHOIS lookup           |
| `--dns`         | Run DNS enumeration        |
| `--subdomains`  | Run subdomain enumeration  |
| `--portscan`    | Run port scanning          |
| `--banner`      | Run banner grabbing        |
| `--tech`        | Run technology detection   |
| `--verbose`     | Enable detailed logging    |
| `--no-html`     | Skip HTML report generation |

---

## 📂 **Output**

Results are saved under `reports/`:
```
reports/
 ├── example.com_whois.txt
 ├── example.com_dns.txt
 ├── example.com_subdomains.txt
 ├── example.com_portscan.txt
 ├── example.com_banner.txt
 ├── example.com_techdetect.txt
 ├── example.com_report_YYYY-MM-DD_HH-MM-SS.html
 └── example.com_timestamp.txt
```
Logs:
```
logs/tool.log
```

---

## 📁 **Directory Structure**
```
ameer-recon-tool/
├── main.py
├── generate_summary.py
├── requirements.txt
├── README.md
├── utils/
│   ├── logger.py
│   ├── report_writer.py
│   └── html_report_writer.py
├── modules/
│   ├── passive/
│   │   ├── whois_lookup.py
│   │   ├── dns_enum.py
│   │   └── subdomain_enum.py
│   └── active/
│       ├── port_scan.py
│       ├── banner_grab.py
│       └── tech_detect.py
├── reports/
├── logs/
└── wordlists/ (optional)
```

---

## ⚠ **Disclaimer**
> 🛡 **For educational use and authorized testing only.**  
> Do not use this tool against systems without explicit permission.

---

## 🙌 **Credits**
Created with ❤️ by **Ameer Hamza**  
*Part of internship red team project*
