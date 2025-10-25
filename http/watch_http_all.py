#!/usr/bin/env python3
import sys, os, subprocess, re, tempfile, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

def run_command_in_bash(command):
    try:
        result = subprocess.run(["bash", "-c", command], capture_output=True, text=True)

        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return False
        
        return result.stdout
    except subprocess.CalledProcessError as exc:
        print("Status: FAIL", exc.returncode, exc.output)

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def create_temp_file(data):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:

        temp_file.write(data)
        return temp_file.name

def httpx(subdomains_array, domain):

    for subdomain in subdomains_array:
        command = f"echo {subdomain} | httpx -silent -json -favicon -fhr -tech-detect -irh -include-chain -timeout 5 -retries 3 -threads 5 -rate-limit 5 -ports 443 -extract-fqdn -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' -H 'Referer: https://{subdomain}' "
    
        print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
        
        results = run_command_in_bash(command)

        if results != '':
            json_obj = json.loads(results)
            upsert_http({
                    "subdomain": subdomain,
                    "scope": domain,
                    "ips": json_obj.get('a', ''),
                    "tech": json_obj.get('tech', []),
                    "title": json_obj.get('title'),
                    "status_code": json_obj.get('status_code', ''),
                    "headers": json_obj.get('header', {}),
                    "url": json_obj.get('url', ''),
                    "final_url": json_obj.get('final_url', ''),
                    "favicon": json_obj.get('favicon', ''),

            })

    return True

if __name__ == "__main__":
    programs = Programs.objects().all()

    for program in programs:
        for scope in program.scopes:
            domain = scope
            obj_lives = LiveSubdomains.objects(scope=domain)
            
            if obj_lives:
                print(f"[{current_time()}] running httpx module for '{domain}' ")

                httpx([obj_live.subdomain for obj_live in obj_lives],domain)
                
            else:
                print(f"[{current_time()}] domain '{domain}' does not exist in watchtower")