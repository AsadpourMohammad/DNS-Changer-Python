import questionary
from rich.console import Console
from rich.table import Table
from rich import box

from dns_utils import get_dns_servers, set_dns_servers, set_dns_servers_to_auto

console = Console()


def get_network_and_servers() -> tuple[str, tuple[str]]:
    current_dns_servers = get_dns_servers()
    current_network_connection = list(current_dns_servers.keys())[0]
    current_dns_servers = current_dns_servers[current_network_connection]

    return current_network_connection, current_dns_servers


def display_active_dns() -> None:
    current_network_connection, current_dns_servers = get_network_and_servers()

    dns_addresses = {
        "Shecan": ("178.22.122.100", "185.51.200.2"),
        "Google": ("8.8.8.8", "8.8.4.4")
    }

    current_dns_servers_name = next(
        (dns_name for dns_name, dns_servers in dns_addresses.items() if dns_servers == current_dns_servers), "Unknown")

    table = Table(title="Current DNS Information", box=box.ROUNDED, show_lines=True)
    table.add_column("Network Connection", style="cyan bold", header_style="light_sky_blue1")
    table.add_column("DNS Servers", style="red3 bold", header_style="light_sky_blue1")
    table.add_column("Provider", style="yellow3 bold", header_style="light_sky_blue1")

    table.add_row(current_network_connection, ", ".join(current_dns_servers), current_dns_servers_name)

    console.print(table)


def setting_dns_servers(choice_dns_servers: tuple[str]) -> None:
    current_network_connection, current_dns_servers = get_network_and_servers()

    dns_addresses = {
        "Shecan": ("178.22.122.100", "185.51.200.2"),
        "Google": ("8.8.8.8", "8.8.4.4")
    }

    current_dns_servers_name = next(
        (dns_name for dns_name, dns_servers in dns_addresses.items() if dns_servers == current_dns_servers), "Unknown")

    choice_dns_servers_name = next(
        (dns_name for dns_name, dns_servers in dns_addresses.items() if dns_servers == choice_dns_servers), "Unknown")

    if current_dns_servers == choice_dns_servers:
        console.print(
            f"[bold red]Your DNS Servers are already set to the specified DNS Servers of[/bold red] "
            f"[cyan]{', '.join(choice_dns_servers)}[/cyan] [bold red]of {choice_dns_servers_name}.[/bold red]")
        return

    table = Table(title="DNS Change Information", box=box.ROUNDED, show_lines=True)
    table.add_column("Current DNS Servers", style="c bold", header_style="light_sky_blue1")
    table.add_column("Current DNS Servers Provider", style="yellow3 bold", header_style="light_sky_blue1")
    table.add_column("New DNS Servers", style="magenta bold", header_style="light_sky_blue1")
    table.add_column("New DNS Servers Provider", style="yellow3 bold", header_style="light_sky_blue1")

    table.add_row(", ".join(current_dns_servers), current_dns_servers_name,
                  ", ".join(choice_dns_servers), choice_dns_servers_name)

    console.print(table)

    choice = questionary.confirm("Do you want to change DNS servers?").ask()

    if choice:
        console.print("\n[bold green]Changing DNS Servers...[/bold green]\n")

        set_dns_servers(current_network_connection, choice_dns_servers)

        console.print("[bold green]DNS Servers changed successfully![/bold green]\n")

        display_active_dns()
    else:
        console.print("\n[bold red]Aborting...[/bold red]")


def clearing_dns_servers() -> None:
    current_network_connection, current_dns_servers = get_network_and_servers()

    print()

    choice = questionary.confirm(
        "Your DNS Servers will be changed to 'Obtain DNS server address automatically'. Do you want to continue?").ask()

    if choice:
        console.print("\n[bold green]Clearing DNS Servers...[/bold green]\n")

        set_dns_servers_to_auto(current_network_connection)

        console.print("[bold green]DNS Servers Cleared successfully![/bold green]\n")

        display_active_dns()
    else:
        console.print("\n[bold red]Aborting...[/bold red]")


def getting_dns_input() -> tuple[str]:
    import re

    def is_dns_server(ip_address: str) -> bool:
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return bool(re.match(pattern, ip_address))

    while True:
        dns_servers = []

        primary_dns_server = questionary.text("Primary DNS Server:",
                                              validate=lambda text:
                                              True if is_dns_server(text) else "Invalid IP Address.").ask()

        dns_servers.append(primary_dns_server)

        secondary_dns_server = questionary.text("Secondary DNS Server:",
                                                validate=lambda text:
                                                True if is_dns_server(text) else "Invalid IP Address.").ask()

        dns_servers.append(secondary_dns_server)
        break

    return tuple(dns_servers)
