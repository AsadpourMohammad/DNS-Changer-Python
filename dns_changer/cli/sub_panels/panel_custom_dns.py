import re
from typing import Union

from questionary import text, confirm

from dns_changer import print_text, get_provider_of_servers
from ...dns.data.json_utils import save_provider_into_json


def custom_dns_panel() -> Union[tuple[str], tuple[str, str], None]:
    def validate_dns_servers(input_dns: str) -> bool:
        validated = bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", input_dns))
        return True if validated else "Invalid IP Address."

    def get_dns(placement) -> str:
        return text(f"{placement} DNS Server:", validate=lambda input_dns: validate_dns_servers(input_dns)).ask()

    primary_dns = get_dns("Primary")

    if not primary_dns:
        return None

    secondary_dns = get_dns("Secondary")

    if not secondary_dns:
        return None

    custom_servers = (primary_dns, secondary_dns)
    custom_servers_provider = get_provider_of_servers(custom_servers)
    if custom_servers_provider == "Unknown":
        _save_dns_panel(custom_servers)
    else:
        print_text(f"Detected DNS Provider: {custom_servers_provider}")

    return custom_servers


def _save_dns_panel(servers: tuple[str, str]):
    print_text("Do you wish to save this DNS Addresses for future use?")

    if confirm("Save DNS Addresses?").ask():
        provider_name = text("Enter a name for the DNS Provider:").ask()

        print_text("\nSaving DNS Addresses...")

        save_provider_into_json(provider_name, servers)

        print_text("DNS Addresses saved successfully!\n")
    else:
        return
