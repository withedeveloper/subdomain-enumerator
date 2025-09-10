#!/usr/bin/env python3
"""
ipextractor.py – Module for IP Extraction and Classification
Team Intruders – Internship Task 2 (Part 4)
"""

import socket
from colorama import Fore, Style
from collections import defaultdict
from os import makedirs, path

# ======================= IP Classification =======================
def classify_ip(ip):
    """Return 'Private' or 'Public' based on IP range."""
    parts = ip.split(".")
    if len(parts) != 4:
        return "Unknown"

    first, second = int(parts[0]), int(parts[1])

    # Private IP ranges
    if first == 10:
        return "Private"
    if first == 172 and 16 <= second <= 31:
        return "Private"
    if first == 192 and second == 168:
        return "Private"
    if first == 127:
        return "Private"  # Loopback

    return "Public"


# ======================= IP Extraction =======================
def extract_ips(subdomains):
    results = []
    ip_to_subs = defaultdict(list)

    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            ip_type = classify_ip(ip)
            ip_to_subs[ip].append(sub)
            results.append((sub, ip, ip_type))
            print(Fore.GREEN + f"[+] {sub:<40} {ip:<15} ({ip_type})" + Style.RESET_ALL)
        except socket.gaierror:
            print(Fore.RED + f"[-] Could not resolve {sub}" + Style.RESET_ALL)

    return results, ip_to_subs


# ======================= Save Results =======================
def save_results(results, ip_to_subs, output_file):
    makedirs(path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        f.write("Subdomain,IP,Type,Shared_With\n")
        for sub, ip, ip_type in results:
            shared = ", ".join([s for s in ip_to_subs[ip] if s != sub])
            f.write(f"{sub},{ip},{ip_type},{shared}\n")

    print(Fore.CYAN + f"\n[✔] IP extraction results saved to {output_file}" + Style.RESET_ALL)


# ======================= CLI for standalone use =======================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IP Extraction & Classification – Team Intruders")
    parser.add_argument("-i", "--input", required=True, help="Input file with live subdomains (one per line)")
    parser.add_argument("-o", "--output", default="output/ip_results.csv", help="File to save IP extraction results")
    args = parser.parse_args()

    # Load subdomains
    try:
        with open(args.input, "r") as f:
            subdomains = [line.strip().split(",")[0] for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] Input file not found: {args.input}" + Style.RESET_ALL)
        exit(1)

    results, ip_to_subs = extract_ips(subdomains)
    save_results(results, ip_to_subs, args.output)

