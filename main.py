import wmi
import subprocess


def get_dns_servers():
    wmi_service = wmi.WMI()
    dns_servers = {}

    for interface in wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if "Virtual" not in interface.Description:
            dns_servers[interface.Description] = interface.DNSServerSearchOrder

    return dns_servers


def set_dns_wmi(adapter_name, dns_servers):
    # Connect to WMI namespace
    wmi_service = wmi.WMI()

    # Get network adapter configuration
    adapter_config = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True, Description=adapter_name)[0]

    # Set DNS servers
    adapter_config.SetDNSServerSearchOrder(dns_servers)


if __name__ == '__main__':
    print(get_dns_servers())

    shecan_dns_servers = ["178.22.122.100", "185.51.200.2"]
    google_dns_servers = ['8.8.8.8', '8.8.4.4']

    current_dns_servers = get_dns_servers()

    for current_adapter_name, dns_server in current_dns_servers.items():
        print(f"\nAdapter '{current_adapter_name}'s current DNS servers are: {dns_server}")
        print(f"Setting DNS servers to {google_dns_servers}\n")
        if "Wi-Fi" in current_adapter_name:
            set_dns_wmi(current_adapter_name, shecan_dns_servers)

    print("Done!")
    print(get_dns_servers())
