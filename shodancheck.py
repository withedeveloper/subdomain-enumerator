#!/usr/bin/env python3
"""
shodancheck.py
Query Shodan for public IPs: open ports + CVEs.
Provides run_shodan(input_file, api_key, output_file)
"""

import csv
from os import makedirs, path
from colorama import Fore, Style, init

init(autoreset=True)


def read_public_ips_from_ipresults(ipresults_csv):
    ips = []
    try:
        with open(ipresults_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # expecting header Subdomain,IP,Type,Shared_With
                if "Type" in row and row["Type"].strip().lower() == "public":
                    ips.append(row.get("IP") or row.get("Ip") or row.get("ip"))
                else:
                    # fallback: if Type column missing, include all
                    if not row.get("Type"):
                        ips.append(row.get("IP") or row.get("Ip") or row.get("ip"))
    except FileNotFoundError:
        raise
    # deduplicate and filter empty
    return sorted({ip.strip() for ip in ips if ip and ip.strip()})


def run_shodan(input_file, api_key, output_file="output/shodan_results.csv"):
    try:
        import shodan
    except Exception as e:
        print(Fore.RED + "[!] Shodan library missing. Install with: pip install shodan" + Style.RESET_ALL)
        raise

    try:
        ips = read_public_ips_from_ipresults(input_file)
    except FileNotFoundError:
        print(Fore.RED + f"[!] IP results file not found: {input_file}" + Style.RESET_ALL)
        return {}

    if not ips:
        print(Fore.YELLOW + "[!] No public IPs found in input file." + Style.RESET_ALL)
        return {}

    api = shodan.Shodan(api_key)
    makedirs(path.dirname(output_file), exist_ok=True)
    results = {}

    for ip in ips:
        try:
            host = api.host(ip)
            ports = host.get("ports", []) or []
            vulns = host.get("vulns", []) or []
            results[ip] = {"ports": ports, "vulns": vulns}
            print(Fore.GREEN + f"\n[+] {ip} – Found {len(ports)} open ports" + Style.RESET_ALL)
            for p in ports:
                print(f"    Port: {p}")
            if vulns:
                print(Fore.RED + "    CVEs:" + Style.RESET_ALL)
                for v in vulns:
                    print(Fore.RED + f"      - {v}" + Style.RESET_ALL)
            else:
                print("    No CVEs found")
        except shodan.APIError as e:
            print(Fore.RED + f"[!] Shodan error for {ip}: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Unexpected error for {ip}: {e}" + Style.RESET_ALL)

    # Save CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Open Ports", "CVEs"])
        for ip, data in results.items():
            writer.writerow([ip, ",".join(map(str, data.get("ports", []))), ",".join(data.get("vulns", []))])

    print(Fore.CYAN + f"[✔] Shodan results saved to {output_file}" + Style.RESET_ALL)
    return results


# CLI support
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Shodan lookup - Team Intruders")
    parser.add_argument("-i", "--input", required=True, help="IP results CSV (from ipextractor.py)")
    parser.add_argument("-k", "--apikey", required=True, help="Shodan API key")
    parser.add_argument("-o", "--output", default="output/shodan_results.csv", help="CSV output")
    args = parser.parse_args()
    run_shodan(args.input, args.apikey, args.output)

