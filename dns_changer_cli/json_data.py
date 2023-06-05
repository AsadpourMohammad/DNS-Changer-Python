import json

from rich.console import Console
from rich.panel import Panel

console = Console()

dns_providers = None


def get_saved_dns_providers():
    global dns_providers

    if dns_providers is None:
        dns_providers = read_dns_providers_from_json()

    return dns_providers


def read_dns_providers_from_json():
    try:
        with open('dnsProviders.json', 'r') as dns_providers_file:
            saved_dns_providers = json.load(dns_providers_file)

        for provider in saved_dns_providers:
            saved_dns_providers[provider] = tuple(saved_dns_providers[provider])

        return saved_dns_providers
    except (FileNotFoundError, json.JSONDecodeError):
        json_err_msg = """
        An error occurred during the loading of DNS Providers JSON file.
        
        Please create a dnsProviders.json file in the same directory as the current script with
        the desired providers and their dns servers if one does not exists, and then try again.
    
        Also, make sure to add the providers in this format:
    
        {
            "Google": ["8.8.8.8", "8.8.4.4"]
        }
        
        You can use the app now, but you will have to enter the DNS servers manually.
        """

        panel = Panel(json_err_msg, title="JSON READING UNSUCCESSFUL", style="bold magenta", width=112)
        console.print(panel)

        return {}
