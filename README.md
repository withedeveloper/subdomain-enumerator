<h1> Subdomain Enumerator – Team Intruders</h1>

A Python-based tool for discovering hidden subdomains using both **brute-force techniques** and **API-based enumeration**.  
eveloped as part of Internship Task 2 by <b>Team Intruders</b>.

---

<h2> Features</h2>

- <b>Brute-force subdomain discovery</b> with wordlist support  
- <b>API-based enumeration</b>:  
- CertSpotter (no API key required)  
- VirusTotal (requires API key)  
- <b>Combined mode</b> – run Brute-force + CertSpotter together  
- <b>Multithreading</b> with configurable thread count (`--threads`)  
- <b>Colored output</b>:
- Green → Valid subdomains with IPs  
- Red → Not found (only in verbose mode)  
- <b>Verbose mode (-v)</b> to show failed attempts  
- <b>Timeout handling</b> (default 3s per DNS request)  
- <b>Progress bar</b> for brute-force enumeration (via tqdm)  
- <b>Results export</b>:  
- CSV (`Subdomain,IP`) for brute-force/combined  
- TXT (list of subdomains) for API results  
-  <b>ASCII banner branding</b> with pyfiglet  

---

<h2> Installation</h2>

<h3>Requirements</h3>

- Python 3.x  

<h3>Install dependencies:</h3>
pip install requests tqdm colorama pyfiglet

<h2> Usage</h2>

Run the tool with different modes:

<h3>🔹 Brute-force Enumeration</h3>

python subenum.py -d example.com -m brute

Custom wordlist & output file:
	python subenum.py -d example.com -m brute -w wordlist.txt -o results.csv

Verbose mode (show not found subdomains):
	python subenum.py -d example.com -m brute -v

Increase threads for faster scanning:
	python subenum.py -d example.com -m brute -t 50

<h3>🔹 API-Based Enumeration</h3>

CertSpotter (no API key needed):
	python subenum.py -d example.com -m certspotter



VirusTotal (requires API key):
	python subenum.py -d example.com -m virustotal -k <your_api_key>

<h3>🔹 Combined Mode</h3>

Run both Brute-force + CertSpotter:
	
python subenum.py -d example.com -m both

<h2> Output</h2> <h3>Terminal (verbose mode with colors):</h3>
Subdomain                                IP
------------------------------------------------------------
Bruteforcing:  45%|█████      | 450/1000 [00:05<00:06, 90.2sub/s]
www.example.com                       93.184.216.34
[-] test.example.com -> Not found
mail.example.com                       93.184.216.34

 <h3>Output file (results.csv):</h3>
 Subdomain,IP
www.example.com,93.184.216.34
mail.example.com,93.184.216.34

 <h3>API output (TXT):</h3>
 Subdomain
www.example.com
mail.example.com

<h2> Authors – Team Intruders</h2>

Threem Amna (Team Lead)

Waqas Ikram (Me)

Azhar Ahmad

Muhamad Arfa

Khansa Kaushaf

Asees Shah

Ammad Hassan

Hamid Iqbal

<h2> Notes</h2>

Default wordlist: wordlist/top1000subdomains.txt

Default output file: output/results.csv

Default threads: 20

Use higher threads (--threads 50) cautiously depending on system performance




