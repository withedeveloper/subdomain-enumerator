<h1>🔎 Subdomain Enumerator – Team Intruders</h1>

A modular Python-based tool for discovering hidden subdomains and identifying which ones are live.  
Developed as part of Internship Task 2 by <b>Team Intruders</b>.

---

<h2>✨ Features</h2>

- 🚀 <b>Brute-force subdomain discovery</b> with wordlist support (multithreaded)  
- 🌍 <b>API-based enumeration</b>:  
  - CertSpotter (no API key required)  
  - VirusTotal (requires API key)  
- 🔗 <b>Combined mode</b> – run Brute-force + CertSpotter together  
- ⚡ <b>Multithreading</b> with configurable thread count (`--threads`)  
- 🎨 <b>Colored output</b>:  
  - 🟢 Green → Valid subdomains with IPs  
  - 🔴 Red → Dead or unresolved subdomains (verbose mode only)  
- 📢 <b>Verbose mode (-v)</b> to show failed attempts  
- ⏱️ <b>Timeout handling</b> (default 3s per DNS/HTTP request)  
- 📊 <b>Progress bar</b> for brute-force enumeration (via tqdm)  
- 💾 <b>Results export</b>:  
  - CSV (`Subdomain,IP`) for brute-force/combined  
  - TXT (list of subdomains) for API results  
  - TXT (list of <b>live subdomains</b>) via livecheck  
- 🎭 <b>ASCII banner branding</b> with pyfiglet  

---

<h2>⚙️ Installation</h2>

<h3>Requirements</h3>

- Python 3.x  

<h3>Install dependencies:</h3>

```bash
pip install requests tqdm colorama pyfiglet

<h2>🚀 Usage</h2> <h3>🔹 Subdomain Enumeration (Part 1 & 2)</h3>

Brute-force enumeration:
	python subdomain_enum.py -d example.com -m brute
	
Brute-force with custom wordlist & output file:
	python subdomain_enum.py -d example.com -m brute -w wordlist.txt -o results.csv

CertSpotter (API, no key needed):
	python subdomain_enum.py -d example.com -m certspotter

VirusTotal (API, requires key):
	python subdomain_enum.py -d example.com -m virustotal -k <your_api_key>

Run both (Brute-force + CertSpotter):
	python subdomain_enum.py -d example.com -m both

<h3>🔹 Live Subdomain Identification (Part 3)</h3>

Check which subdomains are live after enumeration:
	python livecheck.py -i output/results.csv -o output/live_subdomains.txt

Verbose mode (show dead reasons):
	python livecheck.py -i output/results.csv -v

Increase threads for faster live checking:
	python livecheck.py -i output/results.csv -t 50

<h2>📂 Output</h2> <h3>Enumeration results (CSV):</h3>

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

<h2>Authors – Team Intruders</h2>

Threem Amna (Team Lead)

Waqas Ikram (Me)

Asees Shah

Muhammad Arfa

Khansa Kashaf

<h2>Author </h2>

Waqas Ikram

<h2>Notes</h2>

Default wordlist: wordlist/top1000subdomains.txt

Default output file: output/results.csv

Default threads: 20

Live check uses both <b>HTTP</b> and <b>HTTPS</b> probes to confirm activity

Use higher threads (--threads 50) cautiously depending on system performance


