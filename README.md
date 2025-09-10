<h1>Subdomain Enumerator – Team Intruders</h1>

A modular Python-based tool for discovering hidden subdomains, checking which ones are live, and extracting their IP addresses (public or private).  
Developed as part of Internship Task 2 by <b>Team Intruders</b>.

---

<h2>Features</h2>

- <b>Brute-force subdomain discovery</b> with wordlist support (multithreaded)  
- <b>API-based enumeration</b>:  
- CertSpotter (no API key required)  
- VirusTotal (requires API key)  
- <b>Combined mode</b> – run Brute-force + CertSpotter together  
- <b>Multithreading</b> with configurable thread count (`--threads`)  
- <b>Colored output</b>:  
- Green → Valid subdomains with IPs  
- Red → Dead/unresolved subdomains (verbose mode only)  
- <b>Verbose mode (-v)</b> to show failed attempts  
- <b>Timeout handling</b> (default 3s per DNS/HTTP request)  
- <b>Progress bar</b> for brute-force enumeration (via tqdm)  
- <b>Live subdomain filtering</b> (Part 3)  
- <b>IP extraction & classification</b> (Part 4):  
- Detects <b>Private</b> vs <b>Public</b> IPs  
- Identifies origin IP of each subdomain  
- Shows which subdomains share the same IP (shared origin)  
- <b>Results export</b>:  
- CSV (`Subdomain,IP`) for brute-force/combined  
- TXT for API results  
- TXT for live subdomains  
- CSV with `Subdomain,IP,Type,Shared_With` for Part 4  
- <b>ASCII banner branding</b> with pyfiglet  

---

<h2>Installation</h2>

<h3>Requirements</h3>

- Python 3.x  

<h3>Install dependencies:</h3>

```bash
pip install requests tqdm colorama pyfiglet
<h2>Usage</h2> <h3>🔹 Subdomain Enumeration (Part 1 & 2)</h3>

Brute-force enumeration:
	python subdomain_enum.py -d example.com -m brute
	
Custom wordlist & output file:
	python subdomain_enum.py -d example.com -m brute -w wordlist.txt -o results.csv



CertSpotter (API, no key needed):
	python subdomain_enum.py -d example.com -m certspotter

VirusTotal (API, requires key):
	python subdomain_enum.py -d example.com -m virustotal -k <your_api_key>

Run both (Brute-force + CertSpotter):
	python subdomain_enum.py -d example.com -m both

<h3>🔹 Live Subdomain Identification (Part 3)</h3>

Check which subdomains are live:
	python livecheck.py -i output/results.csv -o output/live_subdomains.txt

Verbose mode (show reasons for dead subdomains):
	python livecheck.py -i output/results.csv -v

<h3>🔹 IP Extraction & Classification (Part 4)</h3>

Extract IPs, classify them, and find shared IPs:
	python ipextractor.py -i output/live_subdomains.txt -o output/ip_results.csv

<h2>Output</h2> <h3>Enumeration results (CSV):</h3>
Subdomain,IP
www.example.com,93.184.216.34
mail.example.com,93.184.216.35

<h3>API results (TXT):</h3>
Subdomain
www.example.com
mail.example.com

 <h3>Live subdomains (TXT):</h3>
 www.example.com
mail.example.com

<h3>IP extraction results (CSV):</h3>
Subdomain,IP,Type,Shared_With
www.example.com,93.184.216.34,Public,mail.example.com
mail.example.com,93.184.216.34,Public,www.example.com
internal.example.com,192.168.1.10,Private,

<h2>Authors – Team Intruders</h2>

Threem Amna (Team Lead)

Waqas Ikram (Me)

Azhar Ahmad

Muhamad Arfa

Khansa Kaushaf

Asees Shah

Ammad Hassan

Hamid Iqbal

<h2>Notes</h2>

Default wordlist: wordlist/top1000subdomains.txt

Default output file: output/results.csv

Default threads: 20

Increase threads (--threads 50) cautiously depending on system performance

IP extraction helps identify shared infrastructure and private vs public IPs





