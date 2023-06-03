import wmi


def get_dns_servers():
    c = wmi.WMI()
    dns_servers = {}

    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if "Virtual" not in interface.Description:
            dns_servers[interface.Description] = interface.DNSServerSearchOrder

    return dns_servers


if __name__ == '__main__':
    print(get_dns_servers())
