import os
import json

from dns_changer import TextPanelWrapper, print_panel

_DNS_PROVIDERS = None
_JSON_FILE_PATH = 'dnsProviders.json'


def get_saved_providers() -> dict[str, tuple[str, str]]:
    global _DNS_PROVIDERS

    if _DNS_PROVIDERS is None:
        _DNS_PROVIDERS = _read_dns_providers_from_json()

    return _DNS_PROVIDERS


def save_provider_into_json(provider: str, servers: tuple[str, str]) -> None:
    global _DNS_PROVIDERS

    _DNS_PROVIDERS = get_saved_providers()

    _DNS_PROVIDERS[provider] = servers

    with open(_JSON_FILE_PATH, 'w') as dns_providers_file:
        json.dump(_DNS_PROVIDERS, dns_providers_file, indent=4)


def _read_dns_providers_from_json() -> dict[str, tuple[str, str]]:
    json_err_msg = """
        An error occurred during the loading of DNS Providers JSON file.

        Make sure to add the providers in this format:

        { "Google": ["8.8.8.8", "8.8.4.4"] }

        You can use the app now, but you will have to enter the DNS servers manually.
        """

    if not os.path.isfile(_JSON_FILE_PATH):
        default_providers = {
            'Shecan': ['178.22.122.100', '185.51.200.2'],
            'Google': ['8.8.8.8', '8.8.4.4']
        }

        with open('dnsProviders.json', 'w') as json_file:
            json.dump(default_providers, json_file, indent=4)

    try:
        with open(_JSON_FILE_PATH, 'r') as dns_providers_file:
            saved_dns_providers = json.load(dns_providers_file)

        for provider in saved_dns_providers:
            saved_dns_providers[provider] = tuple(saved_dns_providers[provider])

        return saved_dns_providers
    except (FileNotFoundError, json.JSONDecodeError):
        panel_wrapper = TextPanelWrapper(title="JSON READING UNSUCCESSFUL", text=json_err_msg)
        print_panel(panel_wrapper.panel)

        return {}
