import json
import os

from dns_changer_cli.wrappers.rich_wrappers import TextPanelWrapper, print_panel, print_text

from dns_utils.dns_windows_utils import get_all_networks_and_dns_servers, is_network_dns_auto

__DNS_PROVIDERS__ = None
json_file_path = 'dnsProviders.json'


def get_saved_dns_providers() -> dict[str, tuple[str]]:
    global __DNS_PROVIDERS__

    if __DNS_PROVIDERS__ is None:
        __DNS_PROVIDERS__ = __read_dns_providers_from_json__()

    return __DNS_PROVIDERS__


def get_provider_and_servers_of_network_dns(network: str) -> dict[str, any]:
    """
    Checks to see if the DNS Servers of the selected network match a known provider.
    It can either be a known provider, "Auto" if network is set to auto obtain, or "Unknown" if no match is made.
    """
    servers = get_all_networks_and_dns_servers()[network]

    provider = "Auto" if is_network_dns_auto(network) else get_provider_of_servers(servers)

    return {'provider': provider, 'servers': servers}


def get_provider_of_servers(servers: tuple[str]) -> str:
    return next((provider for provider, dns_servers in get_saved_dns_providers().items() if dns_servers == servers),
                "Unknown")


def save_dns_provider_into_json(provider: str, servers: tuple[str]) -> None:
    global __DNS_PROVIDERS__

    __DNS_PROVIDERS__[provider] = servers

    with open(json_file_path, 'w') as dns_providers_file:
        json.dump(__DNS_PROVIDERS__, dns_providers_file, indent=4)


def __read_dns_providers_from_json__() -> dict[str, tuple[str]]:
    json_err_msg = """
        An error occurred during the loading of DNS Providers JSON file.
        
        Make sure to add the providers in this format:
    
        { "Google": ["8.8.8.8", "8.8.4.4"] }
        
        You can use the app now, but you will have to enter the DNS servers manually.
        """

    if not os.path.isfile(json_file_path):
        default_providers = {
            'Shecan': ['178.22.122.100', '185.51.200.2'],
            'Google': ['8.8.8.8', '8.8.4.4']
        }

        with open('dnsProviders.json', 'w') as json_file:
            json.dump(default_providers, json_file, indent=4)

    try:
        with open(json_file_path, 'r') as dns_providers_file:
            saved_dns_providers = json.load(dns_providers_file)

        for provider in saved_dns_providers:
            saved_dns_providers[provider] = tuple(saved_dns_providers[provider])

        return saved_dns_providers
    except (FileNotFoundError, json.JSONDecodeError):
        panel_wrapper = TextPanelWrapper(title="JSON READING UNSUCCESSFUL", text=json_err_msg)
        print_panel(panel_wrapper.panel)

        return {}
