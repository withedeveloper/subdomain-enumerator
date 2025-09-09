#!/usr/bin/env python3
"""
livecheck.py – Module for Live Subdomain Identification
Team Intruders – Internship Task 2 (Part 3)
"""

import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

# ======================= Check if a single subdomain is live =======================
def check_live(subdomain, timeout=3, verbose=False):
    """
    Check if a subdomain is live by sending HTTP/HTTPS requests.
    Returns True if live, False otherwise.
    """
    urls = [f"http://{subdomain}", f"https://{subdomain}"]
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            if response.status_code < 400:
                print(Fore.GREEN + f"[LIVE] {url} ({response.status_code})" + Style.RESET_ALL)
                return True
        except requests.RequestException as e:
            if verbose:
                print(Fore.RED + f"[DEAD] {url} -> {e.__class__.__name__}" + Style.RESET_ALL)
    return False


# ======================= Filter list of subdomains =======================
def filter_live_subdomains(subdomains, threads=20, timeout=3, verbose=False):
    """
    Takes a list of subdomains, checks which are live, 
    and returns only the live ones.
    """
    live = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda sub: (sub, check_live(sub, timeout, verbose)), subdomains)
        for sub, is_live in results:
            if is_live:
                live.append(sub)
    return live


# ======================= CLI for standalone use =======================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Live Subdomain Checker – Team Intruders")
    parser.add_argument("-i", "--input", required=True, help="Input file with subdomains (one per line)")
    parser.add_argument("-o", "--output", default="output/live_subdomains.txt", help="File to save live subdomains")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default=20)")
    parser.add_argument("--timeout", type=int, default=3, help="Request timeout in seconds (default=3)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed errors for dead subdomains")
    args = parser.parse_args()

    # Read input subdomains
    try:
        with open(args.input, "r") as f:
            subs = [line.strip().split(",")[0] for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] Input file not found: {args.input}" + Style.RESET_ALL)
        exit(1)

    # Check which are live
    print(Fore.CYAN + f"[*] Checking {len(subs)} subdomains for liveness..." + Style.RESET_ALL)
    live = filter_live_subdomains(subs, threads=args.threads, timeout=args.timeout, verbose=args.verbose)

    # Save results
    from os import makedirs, path
    makedirs(path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        for s in live:
            f.write(s + "\n")

    print(Fore.GREEN + f"\n[✔] {len(live)} live subdomains saved to {args.output}" + Style.RESET_ALL)

