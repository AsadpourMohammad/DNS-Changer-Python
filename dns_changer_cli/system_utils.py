import os
import json
import re

from rich.console import Console
from rich.panel import Panel

console = Console()

dns_servers = None


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def read_dns_servers_from_json():
    try:
        with open('dnsAddresses.json', 'r') as dns_addresses_file:
            dns_addresses = json.load(dns_addresses_file)

        for key in dns_addresses:
            dns_addresses[key] = tuple(dns_addresses[key])

        return dns_addresses
    except (FileNotFoundError, json.JSONDecodeError):
        panel = Panel("""
    An error occurred during the loading of DNS addresses JSON file.
    
    Please create a dnsAddresses.json file in the same directory as the current script with the desired 
    networks and dns servers, and then try again.

    You need to add network connections in this format:

    {
        "Google": ["8.8.8.8", "8.8.4.4"]
    }
    
    You can use the app now, but you will have to enter the DNS servers manually.
    """, title="JSON READING UNSUCCESSFUL", style="bold magenta", width=112)

        console.print(panel)

        return {}


def get_all_dns_addresses():
    global dns_servers

    if dns_servers is None:
        dns_servers = read_dns_servers_from_json()

    return dns_servers


def get_dns_addresses_for_provider(provider_name):
    if provider_name in dns_servers:
        return dns_servers[provider_name]
    else:
        raise ValueError("Invalid DNS provider name")


def is_dns_server_valid(ip_address: str) -> bool:
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return bool(re.match(pattern, ip_address))
