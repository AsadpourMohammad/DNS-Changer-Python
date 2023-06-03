import wmi
import subprocess


def get_dns_servers():
    c = wmi.WMI()
    dns_servers = {}

    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if "Virtual" not in interface.Description:
            dns_servers[interface.Description] = interface.DNSServerSearchOrder

    return dns_servers


def set_dns_netsh(interface_name, primary_dns, secondary_dns):
    # Change primary DNS server
    cmd1 = f'netsh interface ipv4 set dns "{interface_name}" static address={primary_dns}'
    subprocess.run(cmd1, shell=True)

    # Change secondary DNS server
    cmd2 = f'netsh interface ipv4 add dns "{interface_name}" address={secondary_dns} index=2'
    subprocess.run(cmd2, shell=True)


if __name__ == '__main__':
    print(get_dns_servers())

    shecan_dns_servers = ["178.22.122.100", "185.51.200.2"]
    google_dns_servers = ['8.8.8.8', '8.8.4.4']

    current_dns_servers = get_dns_servers()

    for current_adapter_name, dns_server in current_dns_servers.items():
        print(f"\nAdapter '{current_adapter_name}'s current DNS servers are: {dns_server}")
        print(f"Setting DNS servers to {google_dns_servers}\n")
        if "Wi-Fi" in current_adapter_name:
            set_dns_netsh("Wi-Fi", google_dns_servers[0], google_dns_servers[1])

    print("Done!")
    print(get_dns_servers())
