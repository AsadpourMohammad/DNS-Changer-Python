import wmi
import winreg

from typing import Dict


# Functions to get and set DNS Servers on windows


def get_all_networks_and_dns_servers() -> Dict[str, tuple[str]]:
    wmi_service = wmi.WMI()

    networks_and_servers = {adaptor.Description: adaptor.DNSServerSearchOrder
                            for adaptor in wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
                            if "Virtual" not in adaptor.Description}

    return networks_and_servers


def get_dns_of_network(network: str) -> Dict[str, tuple[str]]:
    wmi_service = wmi.WMI()

    network = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=network)[0]

    return network.DNSServerSearchOrder


def set_dns_of_network(action: str, network_name: str, dns_servers: tuple[str] = None) -> bool:
    old_dns_servers = get_dns_of_network(network_name)

    wmi_service = wmi.WMI()
    network = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=network_name)[0]
    network.SetDNSServerSearchOrder(dns_servers) if action == "change" else network.SetDNSServerSearchOrder()

    new_dns_servers = get_dns_of_network(network_name)

    return old_dns_servers != new_dns_servers


def is_network_dns_auto(network: str) -> bool:
    wmi_service = wmi.WMI()

    network = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=network)[0]

    interface_key_path = f"SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\{network.SettingID}"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interface_key_path) as key:
            name_server = winreg.QueryValueEx(key, "NameServer")[0]

            if not name_server:
                return True
    except FileNotFoundError:
        pass

    return False
