import wmi
from typing import Dict, List


def get_dns_servers() -> Dict[str, List[str]]:
    wmi_service = wmi.WMI()

    adapter_configs = [config for config in wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
                       if "Virtual" not in config.Description]

    dns_servers = {config.Description: config.DNSServerSearchOrder for config in adapter_configs}

    return dns_servers


def set_dns_servers(adapter_name: str, dns_servers: List[str]) -> None:
    wmi_service = wmi.WMI()

    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    adapter_config.SetDNSServerSearchOrder(dns_servers)
