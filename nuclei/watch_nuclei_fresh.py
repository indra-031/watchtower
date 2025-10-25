#!/usr/bin/env python3
import sys, os, subprocess, re, tempfile, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config
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

def create_temp_file(data):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:

        temp_file.write(data)

        return temp_file.name

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def create_temp_file(data):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:

        temp_file.write(data)

        return temp_file.name

def nuclei(urls):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        for url in urls:
            temp_file.write(f"{url}\n")

    urls_file = temp_file.name

    for subdomain in urls:
        command = f"nuclei -l {urls_file} -config {config().get('WATCH_DIR')}/nuclei/nuclei-public.yaml"
        
        print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
        
        results = run_command_in_bash(command)

        if results != '':
            print(results)
            # json_obj = json.loads(results)
            # upsert_http({
            #         "subdomain": subdomain,
            #         "scope": domain,
            #         "ips": json_obj.get('a', ''),
            #         "tech": json_obj.get('tech', []),
            #         "title": json_obj.get('title'),
            #         "status_code": json_obj.get('status_code', ''),
            #         "headers": json_obj.get('header', {}),
            #         "url": json_obj.get('url', ''),
            #         "final_url": json_obj.get('final_url', ''),
            #         "favicon": json_obj.get('favicon', ''),

            # })

    return True

if __name__ == "__main__":

    https_obj = HttpService.objects().all()

    if https_obj:
        print(f"[{current_time()}] running nuclei module for all http services ")

        nuclei([http_obj.url for http_obj in https_obj])