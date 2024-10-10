import subprocess
import sys
import os

def install_requirements():
    if os.path.exists("requirements.txt"):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("Requirements installed.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Could not install requirements: {str(e)}")
    else:
        print("[!] File requirements.txt not found.")

if __name__ == "__main__":
    install_requirements()

from colorama import Fore, Style, init
import time
import requests
import dns.resolver
import sys
import socket

init()

def type_text(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  

def rgb_gradient(text, start_color, end_color):
    steps = len(text)
    r_step = (end_color[0] - start_color[0]) / steps
    g_step = (end_color[1] - start_color[1]) / steps
    b_step = (end_color[2] - start_color[2]) / steps
    
    for i, char in enumerate(text):
        r = int(start_color[0] + r_step * i)
        g = int(start_color[1] + r_step * i)
        b = int(start_color[2] + r_step * i)
        print(f"\033[38;2;{r};{g};{b}m{char}", end="")
    
    print(Style.RESET_ALL)

def rgb_gradient_char(r, g, b, char):
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

def type_text_with_gradient(text, start_color, end_color, delay=0.05):
    steps = len(text)
    r_step = (end_color[0] - start_color[0]) / steps
    g_step = (end_color[1] - start_color[1]) / steps
    b_step = (end_color[2] - start_color[2]) / steps
    for i, char in enumerate(text):
        r = int(start_color[0] + r_step * i)
        g = int(start_color[1] + g_step * i)
        b = int(start_color[2] + b_step * i)
        print(rgb_gradient_char(r, g, b, char), end="", flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def check_server_status(address):
    url = f"https://api.mcsrvstat.us/3/{address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("online", False):
            players_online = data["players"]["online"] if "players" in data else "Not found"
            players_max = data["players"]["max"] if "players" in data else "Not found"
            port = data.get("port", "Not found")
            ip_address = data.get("ip", "Not found")
            hostname = data.get("hostname", "Not found")
            version = data.get("version", "Not found")
            protocol = data.get("protocol", {}).get("name", "Not found")
            software = data.get("software", "Not found")
            server_id = data.get("serverid", "Not found")
            motd = "\n".join(data.get("motd", {}).get("clean", ["Not found"]))
            plugins = [f"{plugin['name']} v{plugin['version']}" for plugin in data.get("plugins", [])] or "Not found"
            info = "\n".join(data.get("info", {}).get("clean", ["Not found"]))

            type_text_with_gradient(f"\n  Server stats", (255, 0, 0), (0, 0, 255), delay=0.01)
            type_text_with_gradient(f"\nPlayers Online: {players_online}/{players_max}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Port: {port}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"IP Address: {ip_address}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Hostname: {hostname}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Version: {version}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Protocol: {protocol}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Software: {software}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Server ID: {server_id}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"MOTD: {motd}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Plugins: {', '.join(plugins) if isinstance(plugins, list) else plugins}", (255, 0, 0), (0, 0, 255), delay=0.02)
            type_text_with_gradient(f"Info: {info}", (255, 0, 0), (0, 0, 255), delay=0.02)
            time.sleep(1)
            main()

        else:
            print(Fore.RED + "\n\n[!] Server is offline or I was not able to get status from API." + Style.RESET_ALL)
            main()
            
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + "[!] This domain/ip does not exist." + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] An error occurred: {str(e)}" + Style.RESET_ALL)

def dns_scan(domain):
    try:
        type_text_with_gradient(f"\nScanning DNS records for {domain}...", (255, 0, 0), (0, 0, 255), delay=0.02)
        time.sleep(1)

        try:
            a_records = dns.resolver.resolve(domain, 'A')
            type_text_with_gradient("A Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
            for record in a_records:
                type_text_with_gradient(f" - {record.to_text()}", (0, 255, 0), (0, 0, 255), delay=0.02)

        except dns.resolver.NoAnswer:
            type_text_with_gradient("A Records: Not found", (0, 255, 0), (0, 0, 255), delay=0.02)

        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            type_text_with_gradient("AAAA Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
            for record in aaaa_records:
                type_text_with_gradient(f" - {record.to_text()}", (0, 255, 0), (0, 0, 255), delay=0.02)
        except dns.resolver.NoAnswer:
            type_text_with_gradient("AAAA Records: Not found", (0, 255, 0), (0, 0, 255), delay=0.02)

        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            type_text_with_gradient("MX Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
            for record in mx_records:
                type_text_with_gradient(f" - {record.exchange.to_text()} (Preference: {record.preference})", (0, 255, 0), (0, 0, 255), delay=0.02)
        except dns.resolver.NoAnswer:
            type_text_with_gradient("MX Records: Not found", (0, 255, 0), (0, 0, 255), delay=0.02)

        try:
            srv_records = dns.resolver.resolve(domain, 'SRV')
            type_text_with_gradient("SRV Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
            for record in srv_records:
                type_text_with_gradient(f" - {record.target.to_text()}:{record.port} (Priority: {record.priority}, Weight: {record.weight})", (0, 255, 0), (0, 0, 255), delay=0.02)
        except dns.resolver.NoAnswer:
            type_text_with_gradient("SRV Records: Not found", (0, 255, 0), (0, 0, 255), delay=0.02)

    except dns.resolver.NoAnswer:
        print(Fore.RED + "[!] This domain/ip does not exist, or I was not able to find it." + Style.RESET_ALL)
    except dns.resolver.Timeout:
        print(Fore.RED + "[!] DNS query timed out." + Style.RESET_ALL)

def check_host(address):
    max_nodes = 3
    check_types = ['ping', 'http', 'tcp', 'dns', 'udp']
    
    request_ids = {}
    results = {}

    for check_type in check_types:
        url = f"https://check-host.net/check-{check_type}?host={address}&max_nodes={max_nodes}"
        
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            if data.get("ok") == 1:
                request_id = data['request_id']
                request_ids[check_type] = request_id
            else:
                print(Fore.RED + f"[!] Failed to initiate {check_type} check." + Style.RESET_ALL)

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] An error occurred while checking {check_type}: " + str(e) + Style.RESET_ALL)

    for check_type, request_id in request_ids.items():
        result_url = f"https://check-host.net/check-result/{request_id}"
        try:
            result_response = requests.get(result_url, headers={"Accept": "application/json"})
            result_response.raise_for_status()
            results[check_type] = result_response.json()
        
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] An error occurred while fetching results for {check_type}: " + str(e) + Style.RESET_ALL)

    for check_type, result in results.items():
        type_text_with_gradient(f"\nResults for {check_type} check:", (255, 0, 0), (0, 0, 255), delay=0.02)
        for node, checks in result.items():
            type_text_with_gradient(f"Node: {node}", (0, 255, 0), (0, 0, 255), delay=0.02)
            if checks is None:
                print(Fore.RED + "  No results available." + Style.RESET_ALL)
                continue

            if check_type == 'ping':
                for check in checks:
                    type_text_with_gradient(Fore.RED + f"  Status: {check[0]}, Time: {check[1]} seconds, IP: {check[2]}", (0, 255, 0), (0, 0, 255), delay=0.02)
            elif check_type == 'http':
                for check in checks:
                    type_text_with_gradient(Fore.LIGHTCYAN_EX + f"  Status: {check[2]} {check[3]}, IP: {check[4]}, Time: {check[1]} seconds", (0, 255, 0), (0, 0, 255), delay=0.02)
            elif check_type == 'tcp':
                for check in checks:
                    if "error" in check:
                        print(Fore.RED + f"  Error: {check['error']}" + Style.RESET_ALL)
                    else:
                        type_text_with_gradient(Fore.LIGHTCYAN_EX + f"  Connected to IP: {check['address']}, Time: {check['time']} seconds", (0, 255, 0), (0, 0, 255), delay=0.02)
            elif check_type == 'dns':
                for check in checks:
                    for record_type, values in check.items():
                        if isinstance(values, list):  
                            type_text_with_gradient(Fore.LIGHTCYAN_EX + f"  {record_type}: {', '.join(values)}", (0, 255, 0), (0, 0, 255), delay=0.02)
                        else:
                            type_text_with_gradient(Fore.LIGHTCYAN_EX + f"  {record_type}: {values}", (0, 255, 0), (0, 0, 255), delay=0.02)
            elif check_type == 'udp':
                print(Fore.RED + "UDP checks are not implemented (or some error?)." + Style.RESET_ALL)




def main():
    while True:
        type_text_with_gradient("\n\nWelcome to the Minecraft Server Checker!\n", (255, 0, 0), (0, 0, 255), delay=0.02)
        type_text_with_gradient("[1] Full Scan", (255, 0, 0), (0, 0, 255), delay=0.02)
        type_text_with_gradient("[2] Exit", (255, 0, 0), (0, 0, 255), delay=0.02)

        choice = input(Fore.GREEN + "Choose an option: " + Style.RESET_ALL)
        
        if choice == "1":
            ip = input(Fore.CYAN + "Enter the Minecraft server address (domain or IP): " + Style.RESET_ALL)
            dns_scan(ip)
            check_host(ip) 
            check_server_status(ip)
        
        elif choice == "2":
            type_text_with_gradient("See You next time..", (255, 0, 0), (0, 0, 255), delay=0.02)
            sys.exit()
        
        else:
            print(Fore.RED + "[!] Invalid option." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
