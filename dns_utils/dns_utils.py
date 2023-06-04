import wmi
import winreg
from typing import Dict


def get_dns_servers() -> Dict[str, tuple[str]]:
    wmi_service = wmi.WMI()

    adapter_configs = [config for config in wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
                       if "Virtual" not in config.Description]

    dns_servers = {config.Description: config.DNSServerSearchOrder for config in adapter_configs}

    return dns_servers


def get_dns_servers_of_adapter(adapter_name: str) -> Dict[str, tuple[str]]:
    wmi_service = wmi.WMI()

    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    return adapter_config.DNSServerSearchOrder


def set_dns_servers(adapter_name: str, dns_servers: tuple[str]) -> bool:
    pre_dns_servers = get_dns_servers_of_adapter(adapter_name)

    wmi_service = wmi.WMI()
    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]
    adapter_config.SetDNSServerSearchOrder(dns_servers)

    new_dns_servers = get_dns_servers_of_adapter(adapter_name)

    return pre_dns_servers != new_dns_servers


def set_dns_servers_to_auto(adapter_name: str) -> bool:
    pre_dns_servers = get_dns_servers_of_adapter(adapter_name)

    wmi_service = wmi.WMI()
    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]
    adapter_config.SetDNSServerSearchOrder()

    new_dns_servers = get_dns_servers_of_adapter(adapter_name)

    return pre_dns_servers != new_dns_servers


def is_dns_auto_obtain(adapter_name):
    wmi_service = wmi.WMI()

    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    interface_key_path = f"SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\{adapter_config.SettingID}"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interface_key_path) as key:
            name_server = winreg.QueryValueEx(key, "NameServer")[0]

            if not name_server:
                return True
    except FileNotFoundError:
        pass

    return False
