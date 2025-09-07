######################################## Subdomain Enumerator – Team Intruders ####################################################################

A multithreaded subdomain enumeration tool built in Python.
Developed as part of Internship Task 2 by Team Intruders.

==================================================== Features ======================================================================

- Brute-force subdomain discovery using a wordlist

- Multithreading with configurable thread count (--threads)

- Colored output:

- Green → Valid subdomains with IPs

- Red → Not found (shown only in verbose mode)

- Verbose mode (-v) to display failed attempts

- Timeout handling (default 3s per DNS request)

- Progress bar for live tracking of enumeration progress (via tqdm)

- CSV results export (Subdomain,IP)

- ASCII banner branding with pyfiglet

========================== Installation ===========================
Requirements

	Python 3.x

Install dependencies:

	pip install tqdm colorama pyfiglet

======================= Usage ===================================
Basic usage (default settings):
	python bruteforce.py -d example.com

Custom wordlist & output file:
	python bruteforce.py -d example.com -w wordlist.txt -o results.csv

Verbose mode (show not found subdomains):
	python bruteforce.py -d example.com -v

Increase threads for faster scanning:
	python bruteforce.py -d example.com -t 50

========================== Output ================================
Terminal (verbose mode with colors):
		Subdomain                                IP
	------------------------------------------------------------
	Checking subdomains:  45%|█████      | 450/1000 [00:05<00:06, 90.2sub/s]
	www.example.com                       93.184.216.34
	[-] test.example.com -> Not found
	mail.example.com                       93.184.216.34


Output file (results.csv):
	Subdomain,IP
	www.example.com,93.184.216.34
	mail.example.com,93.184.216.34


======================== Authors (Team Intruders) =========================

1) Threem Amna (Team Lead)

2) Waqas Ikram (Me)

3) Azhar Ahmad

4) Muhamad Arfa

5) Khansa Kaushaf

6) Asees Shah

7) Ammad Hassan

8) Hamid Iqbal

================================ Notes ==================================

Default wordlist: wordlist/top1000subdomains.txt

Default output file: output/results.csv

Default threads: 20

Increase threads with caution (e.g., --threads 50) depending on system performance.


