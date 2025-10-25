#!/usr/bin/env python3
import sys, re, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *
from config import config

WATCH_DIR = config().get("WATCH_DIR")

class Colors:
    GRAY ="\033[90m"
    RESET ="\033[0m"

def ns_brute(domain):
    # Paths for temporary files
    best_dns_path = os.path.join(WATCH_DIR, "best-dns-wordlist.txt")
    subdomains_path = os.path.join(WATCH_DIR, "2m-subdomains.txt")
    crunch_path = os.path.join(WATCH_DIR, "4-lower.txt")
    static_words_path = os.path.join(WATCH_DIR, "static-finals.txt")
    domain_static_path = os.path.join(WATCH_DIR, f"{domain}.static")
    dns_brute = os.path.join(WATCH_DIR, f"{domain}.dns_brute")
    dns_gen_words = os.path.join(WATCH_DIR, "dnsgen-words.txt")
    alt_dns_words = os.path.join(WATCH_DIR, "altdns-words.txt")
    merged_path = os.path.join(WATCH_DIR, "words-merged.txt")
    domain_dns_gen = os.path.join(WATCH_DIR, f"{domain}.dns_gen")

    try:
        # Step 1: Prepare wordlist for static brute
        commands = [
            f"curl -s https://wordlist-cdn-assetnote.io/data/manual/best-dns-wordlist.txt -o {best_dns_path}",
            f"curl -s https://wordlist-cdn-assetnote.io/data/manual/2m-subdomains.txt -o {subdomains_path}",
            f"crunch 1 4 abcdefghijklmnopqrstuvwxyz1234567890 > {crunch_path}",
            f"cat {best_dns_path} {subdomains_path} {crunch_path} | sort -u > {static_words_path}",
            f"awk -v domain='{domain}' '{{print $0\".\"domain}}' {static_words_path} > {domain_static_path}",
        ]
        for cmd in commands:
            print(f"{Colors.GRAY}Executing command: {cmd}{Colors.RESET}")
            run_command_in_bash(cmd)

        # Step 2: Run shuffledns
        shuffledns_command = (
            f"shuffledns -list {domain_static_path} -d {domain} -r ~/.resolvers"
            f"-m $(which massdns) -mode resolve -t 30 -silent > {dns_brute}"
        )
        print(f"{Colors.GRAY}Executing command: {shuffledns_command}{Colors.RESET}")   
        run_command_in_bash(shuffledns_command)

        # Step 3: Prepare wordlist for dynamic brute
        commands = [
            f"curl -s https://raw.githubusercontent.com/AlephNullsk/dnsgen/master/dnsgen/words.txt -o {dns_gen_words}",
            f"curl -s https://raw.githubusercontent.com/infosec-au/altdns/master/words.txt -o {alt_dns_words}",
            f"cat {dns_gen_words} {alt_dns_words} | sort -u > {merged_path}",
            f"subfinder -d {domain} -all | dnsx -silent | anew {dns_brute}",
            f"cat {dns_brute} | dnsgen -w {merged_path} > {domain_dns_gen}"
        ]
        for cmd in commands:
            print(f"{Colors.GRAY}Executing command: {cmd}{Colors.RESET}")           
            run_command_in_bash(cmd)

        # Step 4: Run shuffledns
        shuffledns_command = (
            f"shuffledns -list {domain_dns_gen} -d {domain} -r ~/.resolvers"
            f"-m $(which massdns) -mode resolve -t 30 -silent | anew {dns_brute}"
        )
        print(f"{Colors.GRAY}Executing command: {shuffledns_command}{Colors.RESET}")           
        run_command_in_bash(shuffledns_command)

        with open(dns_brute, "r") as file:
            result = [line.strip() for line in file.readlines()]
        return result
    
    finally:
        # Clean up temporary files
        for file_path in [
            best_dns_path,
            subdomains_path,
            crunch_path,
            static_words_path,
            domain_static_path,
            dns_brute,
            dns_gen_words,
            alt_dns_words,
            merged_path,
            domain_dns_gen,
        ]:
            if os.path.exists(file_path):
                print(f"{Colors.GRAY}Removing file: {file_path}{Colors.RESET}")
                os.remove(file_path)

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if not domain:
        print(f"Usage: watch_ns_brute domain")
        sys.exit()

    program = get_program_by_scope(domain)

    if program:
        print(f"[{current_time()}] running ns_brute module for '{domain}'")
        subs = ns_brute(domain)
        for sub in subs:
            if re.search(r"\.\s*" + re.escape(domain), sub, re.IGNORECASE):
                upsert_subdomain(program.program_name, sub, "ns_brute")
                upsert_lives(domain=domain, subdomain=sub, ips=[])
    else:
        print(f"[{curretn_time()}] scope for '{domain}' does not exist in watchtower")