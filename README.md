# watchtower
welcome to my watchtower :)

## setup th watch
1. inside the database folder run `docker compose up -d`
2. modify the config/.env file
3. install requirements
```bash
pip3 install -r requirements.txt 
```
if you get error for not having virtualenv you can install them one by one with
```bash
apt install python3-xyz
```
4. configure zsh or bash alias variables

## bashrc configurations
add following lines to your `~/bashrc` file:
```bash
alias watch_sync_programs="/home/indra/Projects/watchtower/programs/watch_sync_programs.py"
alias watch_subfinder="/home/indra/Projects/watchtower/enum/watch_subfinder.py"
alias watch_crtsh="/home/indra/Projects/watchtower/enum/watch_crtsh.py"
alias watch_abuseipdb="/home/indra/Projects/watchtower/enum/watch_abuseipdb.py"
alias watch_enum_all="/home/indra/Projects/watchtower/enum/watch_enum_all.py"
alias watch_ns="/home/indra/Projects/watchtower/ns/watch_ns.py"
alias watch_ns_all="/home/indra/Projects/watchtower/ns/watch_ns_all.py"
alias watch_httpx="/home/indra/Projects/watchtower/http/watch_httpx.py"
alias watch_http_all="/home/indra/Projects/watchtower/http/watch_http_all.py"
alias watch_nuclei_all="/home/indra/Projects/watchtower/nuclei/watch_nuclei_all.py"
```
5. get permision to alias files
```bash
chmod +x /home/indra/Projects/watchtower/programs/*
chmod +x /home/indra/Projects/watchtower/enum/*
chmod +x /home/indra/Projects/watchtower/ns/*
chmod +x /home/indra/Projects/watchtower/http/*
chmod +x /home/indra/Projects/watchtower/nuclei/*
```

6. run with this command
```bash
python3 app.py
```
