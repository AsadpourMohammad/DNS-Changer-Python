from .json_utils import get_saved_providers
from ..utils.dns_windows_utils import get_all_networks_and_dns_servers, is_network_dns_auto


def get_provider_and_servers_of_network_dns(network: str) -> dict[str, any]:
    """
    Checks to see if the DNS Servers of the selected network match a known provider.
    It can either be a known provider, "Auto" if network is set to auto obtain, or "Unknown" if no match is made.
    """
    servers = get_all_networks_and_dns_servers()[network]

    provider = "Auto" if is_network_dns_auto(network) else get_provider_of_servers(servers)

    return {'provider': provider, 'servers': servers}


def get_provider_of_servers(dns_servers: tuple[str, str]) -> str:
    return next((provider for provider, servers in get_saved_providers().items() if dns_servers == servers), "Unknown")
