from colorama import Fore, Style, init
import time
import requests
import dns.resolver

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

            type_text_with_gradient(f"Players Online: {players_online}/{players_max}", (255, 0, 0), (0, 0, 255), delay=0.02)
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

            type_text_with_gradient("\nScanning DNS...\n", (255, 165, 0), (0, 0, 255), delay=0.05)
            time.sleep(1)

        else:
            print(Fore.RED + "[!] Server is offline." + Style.RESET_ALL)
            
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + "[!] This domain/ip does not exist." + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] An error occurred: {str(e)}" + Style.RESET_ALL)

def dns_scan(domain):
    try:
        type_text_with_gradient(f"Scanning DNS records for {domain}...", (255, 0, 0), (0, 0, 255), delay=0.02)
        time.sleep(1)

        a_records = dns.resolver.resolve(domain, 'A')
        type_text_with_gradient("A Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
        for record in a_records:
            type_text_with_gradient(f" - {record.to_text()}", (0, 255, 0), (0, 0, 255), delay=0.02)

        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            type_text_with_gradient("AAAA Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
            for record in aaaa_records:
                type_text_with_gradient(f" - {record.to_text()}", (0, 255, 0), (0, 0, 255), delay=0.02)
        except dns.resolver.NoAnswer:
            type_text_with_gradient("AAAA Records: Not found", (0, 255, 0), (0, 0, 255), delay=0.02)

        mx_records = dns.resolver.resolve(domain, 'MX')
        type_text_with_gradient("MX Records:", (0, 255, 0), (0, 0, 255), delay=0.02)
        for record in mx_records:
            type_text_with_gradient(f" - {record.exchange.to_text()} (Preference: {record.preference})", (0, 255, 0), (0, 0, 255), delay=0.02)

    except dns.resolver.NoAnswer:
        print(Fore.RED + "[!] This domain/ip does not exist." + Style.RESET_ALL)
    except dns.resolver.Timeout:
        print(Fore.RED + "[!] DNS query timed out." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] An error occurred during DNS scan: {str(e)}" + Style.RESET_ALL)

def full_scan():
    start_color = (255, 0, 0)  
    end_color = (0, 0, 255)    
    rgb_gradient("[!] Server Domain/IP: ", start_color, end_color)  
    ip = input("").strip()

    if not all(part.isdigit() for part in ip.split(".")) or len(ip.split(".")) != 4:
        dns_scan(ip)  
    else:
        print(Fore.YELLOW + "[*] Input is an IP address; skipping DNS scan." + Style.RESET_ALL)

    type_text_with_gradient("Connecting to api..", start_color, end_color, delay=0.05)
    time.sleep(1)
    check_server_status(ip) 

def main():
    start_color = (255, 0, 0)  
    end_color = (0, 0, 255)    

    print(Fore.GREEN + "\n\nWelcome, choose an option to continue:\n" + Style.RESET_ALL)
    rgb_gradient("[1] Full scan\n", start_color, end_color)
    option = int(input(Fore.GREEN + "Your option: " + Style.RESET_ALL))

    if option == 1:
        full_scan()
    else:
        print(Fore.RED + "\nChoose valid option.\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
