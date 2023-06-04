import json

from rich.console import Console
from rich.panel import Panel

console = Console()

dns_servers = None


def read_dns_servers_from_json():
    try:
        with open('dnsAddresses.json', 'r') as dns_addresses_file:
            dns_addresses = json.load(dns_addresses_file)

        for key in dns_addresses:
            dns_addresses[key] = tuple(dns_addresses[key])

        return dns_addresses
    except (FileNotFoundError, json.JSONDecodeError):
        json_err_msg = """
        An error occurred during the loading of DNS addresses JSON file.
        
        Please create a dnsAddresses.json file in the same directory as the current script with
        the desired networks and dns servers if one does not exists, and then try again.
    
        Also, make sure to add the network connections in this format:
    
        {
            "Google": ["8.8.8.8", "8.8.4.4"]
        }
        
        You can use the app now, but you will have to enter the DNS servers manually.
        """

        panel = Panel(json_err_msg, title="JSON READING UNSUCCESSFUL", style="bold magenta", width=112)
        console.print(panel)

        return {}


def get_all_dns_addresses():
    global dns_servers

    if dns_servers is None:
        dns_servers = read_dns_servers_from_json()

    return dns_servers
