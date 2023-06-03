from dns_utils import get_dns_servers, set_dns_servers, set_dns_servers_to_auto


def display_active_dns() -> None:
    current_dns_servers = get_dns_servers()
    current_network_connection = list(current_dns_servers.keys())[0]
    current_dns_servers = current_dns_servers[current_network_connection]

    dns_addresses = {
        "Shecan": ("178.22.122.100", "185.51.200.2"),
        "Google": ("8.8.8.8", "8.8.4.4")
    }

    current_dns_servers_name = next(
        (dns_name for dns_name, dns_servers in dns_addresses.items() if dns_servers == current_dns_servers), "Unknown")

    print(f"""
Your current active Network Connection is:

    {current_network_connection}

Your current DNS Servers are:

    {', '.join(current_dns_servers)}

DNS Servers provided by 
    
    {current_dns_servers_name}
""")


def setting_dns_servers(choice_dns_servers: tuple[str]) -> None:
    current_dns_servers = get_dns_servers()
    current_network_connection = list(current_dns_servers.keys())[0]
    current_dns_servers = current_dns_servers[current_network_connection]

    display_active_dns()

    if current_dns_servers == choice_dns_servers:
        print(f"""
Your DNS Servers are already set to the specified DNS Servers of

    {', '.join(choice_dns_servers)}
    """)

        return

    print(f"""
Your DNS Servers will be changed to:

    {', '.join(choice_dns_servers)}

Are you sure you want to continue? (y/n)
    """)

    choice = input("> ").lower()

    if choice == "y":
        print("\nChanging DNS Servers...")

        set_dns_servers(current_network_connection, choice_dns_servers)

        print("DNS Servers changed successfully!")

        display_active_dns()
    elif choice == "n":
        print("Aborting...")
    else:
        print("Invalid choice. Aborting...")


def clearing_dns_servers() -> None:
    current_dns_servers = get_dns_servers()

    current_network_connection = list(current_dns_servers.keys())[0]
    current_dns_servers = current_dns_servers[current_network_connection]

    display_active_dns()

    print(f"""
Your DNS Servers will be changed to 'Obtain DNS server address automatically'

Are you sure you want to continue? (y/n)
            """)
    choice = input("> ").lower()

    if choice == "y":
        print("\nChanging DNS Servers...")

        set_dns_servers_to_auto(current_network_connection)

        print("DNS Servers changed successfully!")

        display_active_dns()
    elif choice == "n":
        print("Aborting...")
    else:
        print("Invalid choice. Aborting...")


def getting_dns_input() -> tuple[str]:
    import re

    def is_dns_server(ip_address: str) -> bool:
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return bool(re.match(pattern, ip_address))

    dns_servers = []

    while True:
        primary_dns_server = input("Primary DNS Server: ")

        if is_dns_server(primary_dns_server):
            dns_servers.append(primary_dns_server)
        else:
            print("Invalid IP Address. Try again...")
            continue

        secondary_dns_server = input("Secondary DNS Server: ")

        if is_dns_server(secondary_dns_server):
            dns_servers.append(secondary_dns_server)
        else:
            print("Invalid IP Address. Try again...")
            continue

        break

    return tuple(dns_servers)
