#!/usr/bin/env python3
import socket
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from os import makedirs, path
from tqdm import tqdm
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Global settings
socket.setdefaulttimeout(3)
init(autoreset=True)  # Auto reset colors after each print

# ======================= Banner ===========================
def show_banner():
    f = Figlet(font="slant")
    title = f.renderText("SUBDOMAIN ENUMERATOR")
    team = f.renderText("TEAM INTRUDERS")
    print(Fore.MAGENTA + title + Style.RESET_ALL)
    print(Fore.CYAN + "Developed by\n" + team + Style.RESET_ALL)

# ======================= Brute-force Enumeration ===========================
def resolve_subdomain(word, domain, verbose=False):
    url = f"{word}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        return url, ip
    except socket.gaierror:
        if verbose:
            print(Fore.RED + f"[-] {url} -> Not found" + Style.RESET_ALL)
        return None


def bruteforce_enum(domain, wordlist, verbose=False, threads=20):
    try:
        with open(wordlist, "r") as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + f"[!] Wordlist not found: {wordlist}" + Style.RESET_ALL)
        return []

    print(Fore.CYAN + f"[*] Starting brute-force enumeration for {domain}..." + Style.RESET_ALL)
    subdomains = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(resolve_subdomain, word, domain, verbose) for word in words]
        for future in tqdm(futures, desc="Bruteforcing", unit="sub"):
            result = future.result()
            if result:
                subdomains.append(result)

    return subdomains

# ======================= API Enumeration ===========================
def enum_certspotter(domain):
    url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
    subdomains = set()

    print(Fore.CYAN + "[*] Fetching from CertSpotter..." + Style.RESET_ALL)
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        for item in response.json():
            for dns in item.get("dns_names", []):
                if domain in dns:
                    subdomains.add(dns.lstrip("*."))
    else:
        print(Fore.RED + f"[!] CertSpotter error {response.status_code}: {response.text}" + Style.RESET_ALL)
    return sorted(subdomains)


def enum_virustotal(domain, api_key):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"
    headers = {"x-apikey": api_key}
    subdomains = []

    print(Fore.CYAN + "[*] Fetching from VirusTotal..." + Style.RESET_ALL)
    while url:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(Fore.RED + f"[!] VirusTotal error {response.status_code}: {response.text}" + Style.RESET_ALL)
            break

        data = response.json()
        for item in data.get("data", []):
            subdomains.append(item["id"])

        url = data.get("links", {}).get("next")  # pagination

    return sorted(set(subdomains))

# ======================= Save Results ===========================
def save_results(subdomains, output_file, api_mode=False):
    makedirs(path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        if api_mode:
            f.write("Subdomain\n")
            for s in subdomains:
                f.write(s + "\n")
        else:
            f.write("Subdomain,IP\n")
            for sub, ip in subdomains:
                f.write(f"{sub},{ip}\n")
    print(Fore.GREEN + f"\n[✔] Results saved to {output_file}" + Style.RESET_ALL)

# ======================= Main CLI ===========================
def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumerator (Brute-force + API) - Team Intruders")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-m", "--method", required=True,
                        choices=["brute", "certspotter", "virustotal", "both"],
                        help="Enumeration method to use")
    parser.add_argument("-w", "--wordlist", default="wordlist/top1000subdomains.txt", help="Wordlist for brute-force")
    parser.add_argument("-o", "--output", default="output/results.txt", help="File to save results")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Threads for brute-force (default=20)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output (for brute-force)")
    parser.add_argument("-k", "--apikey", help="API key (required for VirusTotal)")
    args = parser.parse_args()

    # Show banner
    show_banner()

    # Run selected method(s)
    if args.method == "brute":
        results = bruteforce_enum(args.domain, args.wordlist, args.verbose, args.threads)
        for sub, ip in results:
            print(Fore.GREEN + f"[+] {sub:<40} {ip}" + Style.RESET_ALL)
        save_results(results, args.output)

    elif args.method == "certspotter":
        subs = enum_certspotter(args.domain)
        for s in subs:
            print(Fore.GREEN + " - " + s + Style.RESET_ALL)
        save_results(subs, args.output, api_mode=True)

    elif args.method == "virustotal":
        if not args.apikey:
            print(Fore.RED + "[!] API key required for VirusTotal (-k/--apikey)" + Style.RESET_ALL)
            return
        subs = enum_virustotal(args.domain, args.apikey)
        for s in subs:
            print(Fore.GREEN + " - " + s + Style.RESET_ALL)
        save_results(subs, args.output, api_mode=True)

    elif args.method == "both":
        print(Fore.YELLOW + "[*] Running both brute-force and CertSpotter..." + Style.RESET_ALL)
        brute_res = bruteforce_enum(args.domain, args.wordlist, args.verbose, args.threads)
        api_res = enum_certspotter(args.domain)
        all_subs = set([s for s, _ in brute_res] + api_res)

        for s in sorted(all_subs):
            print(Fore.GREEN + " - " + s + Style.RESET_ALL)

        save_results(sorted(all_subs), args.output, api_mode=True)


if __name__ == "__main__":
    main()

