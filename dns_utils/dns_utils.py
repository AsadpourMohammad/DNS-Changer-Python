import wmi
from typing import Dict


def get_dns_servers() -> Dict[str, tuple[str]]:
    wmi_service = wmi.WMI()

    adapter_configs = [config for config in wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
                       if "Virtual" not in config.Description]

    dns_servers = {config.Description: config.DNSServerSearchOrder for config in adapter_configs}

    return dns_servers


def set_dns_servers(adapter_name: str, dns_servers: tuple[str]) -> None:
    wmi_service = wmi.WMI()

    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    adapter_config.SetDNSServerSearchOrder(dns_servers)


def set_dns_servers_to_auto(adapter_name: str) -> None:
    wmi_service = wmi.WMI()

    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    adapter_config.SetDNSServerSearchOrder()
