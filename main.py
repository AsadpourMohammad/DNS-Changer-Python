import subprocess
import re


def get_dns_servers():
    output = subprocess.check_output("ipconfig /all", shell=True, text=True)

    current_interface = ""
    media_disconnected = False
    dns_servers = {}

    for line in output.splitlines():
        if "adapter" in line:
            current_interface = line.strip().rstrip(':')
            media_disconnected = False
            if "(WSL)" in current_interface:
                current_interface = ""
                continue
        elif "Media State" in line:
            media_disconnected = "Media disconnected" in line
        elif "IPv4 Address" in line and not media_disconnected and current_interface:
            dns_servers[current_interface] = None
        elif "DNS Servers" in line:
            dns_ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if dns_ips:
                dns_servers[current_interface] = dns_ips
        elif dns_servers.get(current_interface) is not None:
            additional_dns_ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            if additional_dns_ips:
                dns_servers[current_interface].extend(additional_dns_ips)

    return dns_servers


if __name__ == '__main__':
    print(get_dns_servers())
