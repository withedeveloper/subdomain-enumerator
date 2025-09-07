#!/usr/bin/env python3

import socket
from pyfiglet import Figlet
import argparse
from concurrent.futures import ThreadPoolExecutor
from os import makedirs, path
from tqdm import tqdm
from colorama import Fore, Style, init

# Global settings
socket.setdefaulttimeout(3)
init(autoreset=True)  # Auto reset colors after each print

# =================== Display Starting banner =======================
f = Figlet(font="slant")
title = f.renderText("SUBDOMAIN ENUMERATOR")
team = f.renderText("Team Intruders")
print(title, "\nDeveloped by\n", team)

# =========================== Get Command Line Args ==================
def get_args():
    parser = argparse.ArgumentParser(description="Subdomain Enumerator - Team Intruders")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", default="wordlist/top1000subdomains.txt", help="Path to wordlist")
    parser.add_argument("-o", "--output", default="output/results.csv", help="File to save results (CSV format)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default=20)")
    return parser.parse_args()

# ======================= Helper function for verbose =====================
def vprint(msg, verbose):
    if verbose:
        print(msg)

# ======================= Helper function for threading ====================
def resolve_subdomain(word, domain, verbose=False):
    url = f"{word}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        return url, ip
    except socket.gaierror:
        vprint(Fore.RED + f"[-] {url} -> Not found" + Style.RESET_ALL, verbose)
        return None

# ==================== Main checking logic ====================
def check_subdomain(domain, wordlist, output_file, verbose, threads):
    try:
        with open(wordlist, 'r') as wlist:
            words = wlist.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + "[!] Wordlist not found!" + Style.RESET_ALL)
        return []

    print(f"{'Subdomain':<40} {'IP':<20}")
    print("-" * 60)

    subdomains = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(resolve_subdomain, word, domain, verbose) for word in words]

        for future in tqdm(futures, desc="Checking subdomains", unit="sub"):
            result = future.result()
            if result:
                sub, ip = result
                print(Fore.GREEN + f"{sub:<40} {ip:<20}" + Style.RESET_ALL)
                subdomains.append((sub, ip))

    # Save results in CSV
    makedirs(path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as outfile:
        outfile.write("Subdomain,IP\n")
        for sub, ip in subdomains:
            outfile.write(f"{sub},{ip}\n")

    print(Fore.CYAN + f"\n[✔] Results saved to {output_file}" + Style.RESET_ALL)

# ==================== Entry Point ====================
if __name__ == "__main__":
    args = get_args()
    check_subdomain(args.domain, args.wordlist, args.output, args.verbose, args.threads)

