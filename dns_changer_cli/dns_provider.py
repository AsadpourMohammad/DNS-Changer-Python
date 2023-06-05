import json

from dns_changer_cli.wrappers.rich_wrappers import TextPanelWrapper, print_panel, print_text

from dns_utils.dns_windows_utils import get_all_networks_and_dns_servers, is_network_dns_auto

__DNS_PROVIDERS__ = None


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


def __read_dns_providers_from_json__() -> dict[str, tuple[str]]:
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
    
    try:
        with open('dnsProviders.json', 'r') as dns_providers_file:
            saved_dns_providers = json.load(dns_providers_file)

        for provider in saved_dns_providers:
            saved_dns_providers[provider] = tuple(saved_dns_providers[provider])

        return saved_dns_providers
    except (FileNotFoundError, json.JSONDecodeError):
        panel_wrapper = TextPanelWrapper(title="JSON READING UNSUCCESSFUL", text=json_err_msg)
        print_panel(panel_wrapper.panel)

        return {}
