from typing import Union, Tuple

import questionary
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns

from questionary import Style

from dns_utils.dns_utils import get_dns_servers, set_dns_servers, set_dns_servers_to_auto, is_dns_auto_obtain
from dns_changer_cli.system_utils import get_all_dns_addresses

console = Console()


def get_network_and_servers() -> list[tuple[str, tuple[str]]]:
    current_dns_servers = get_dns_servers()
    network_and_servers = []

    for network_connection in current_dns_servers:
        dns_servers = current_dns_servers[network_connection]
        network_and_servers.append((network_connection, dns_servers))

    return network_and_servers


def select_network_connection(network_and_servers):
    network_choices = [network_connection for network_connection, _ in network_and_servers]
    selected_network = questionary.select("Select the network connection:", choices=network_choices,
                                          style=Style(
                                              [
                                                  ("qmark", "fg:#673ab7 bold"),
                                                  ('highlighted', 'fg:#d70000 bold'),
                                                  ("pointer", "fg:#d70000 bold"),
                                                  ('text', 'fg:#d7ffff bold'),
                                                  ("answer", "fg:#afd7ff bold"),
                                              ]
                                          )).ask()

    return selected_network


def display_active_dns() -> None:
    network_and_servers = get_network_and_servers()

    table = Table(title="Current DNS Information", box=box.ROUNDED, show_lines=True)
    table.add_column("Network Connection", style="cyan bold", header_style="light_sky_blue1")
    table.add_column("DNS Servers", style="red3 bold", header_style="light_sky_blue1")
    table.add_column("Provider", style="yellow3 bold", header_style="light_sky_blue1")

    for network_connection, dns_servers in network_and_servers:
        dns_servers_name = "Auto" if is_dns_auto_obtain(network_connection) else next(
            (dns_name for dns_name, servers in get_all_dns_addresses().items() if servers == dns_servers), "Unknown")

        table.add_row(network_connection, ", ".join(dns_servers), dns_servers_name)

    panel = Panel(renderable=table, title="DNS Changer Application", style="bold", title_align="left",
                  border_style="cyan bold", padding=(1, 5))

    console.print(Columns([panel], align="center"))


def setting_dns_servers(choice_dns_servers: tuple[str]) -> None:
    network_and_servers = get_network_and_servers()

    if not network_and_servers:
        console.print("[bold red]No active network connections found![/bold red]\n")
        return

    selected_network = select_network_connection(network_and_servers)

    if not selected_network:
        console.print("[bold red]Aborting...[/bold red]\n")
        return

    current_dns_servers = get_dns_servers()[selected_network]

    current_dns_servers_name = "Auto" if is_dns_auto_obtain(selected_network) else next(
        (dns_name for dns_name, dns_servers in get_all_dns_addresses().items() if dns_servers == current_dns_servers),
        "Unknown")

    choice_dns_servers_name = next(
        (dns_name for dns_name, dns_servers in get_all_dns_addresses().items() if dns_servers == choice_dns_servers),
        "Unknown")

    if current_dns_servers == choice_dns_servers:
        console.print(
            f"[bold red]Your DNS Servers are already set to the specified DNS Servers of[/bold red] "
            f"[cyan]{', '.join(choice_dns_servers)}[/cyan] [bold red]of {choice_dns_servers_name}.[/bold red]")
        return

    table = Table(title=f"DNS Change Information for network '{selected_network}'", box=box.ROUNDED, show_lines=True)

    table.add_column("Current DNS Servers",
                     style="cyan bold", header_style="light_sky_blue1", justify="center", vertical="middle")
    table.add_column("Current Provider",
                     style="yellow3 bold", header_style="light_sky_blue1", justify="center", vertical="middle")
    table.add_column("New DNS Servers",
                     style="magenta bold", header_style="light_sky_blue1", justify="center", vertical="middle")
    table.add_column("New Provider",
                     style="yellow3 bold", header_style="light_sky_blue1", justify="center", vertical="middle")

    new_line = '\n'
    table.add_row(f"{new_line}".join(current_dns_servers), current_dns_servers_name,
                  f"{new_line}".join(choice_dns_servers), choice_dns_servers_name)

    panel = Panel(renderable=table, title="DNS Changer Application", style="bold", title_align="left",
                  border_style="cyan bold", padding=(1, 5))

    console.print(Columns([panel]))

    choice = questionary.confirm("Do you want to change DNS servers?").ask()

    if choice:
        console.print("\n[bold green]Changing DNS Servers...[/bold green]\n")

        set_dns_servers(selected_network, choice_dns_servers)

        console.print("[bold green]DNS Servers changed successfully![/bold green]\n")

        display_active_dns()
    else:
        console.print("\n[bold red]Aborting...[/bold red]")


def clearing_dns_servers() -> None:
    network_and_servers = get_network_and_servers()

    if not network_and_servers:
        console.print("[bold red]No active network connections found![/bold red]\n")
        return

    print()

    selected_network = select_network_connection(network_and_servers)

    if not selected_network:
        console.print("[bold red]Aborting...[/bold red]\n")
        return

    choice = questionary.confirm(
        "Your DNS Servers will be changed to 'Obtain DNS server address automatically'. Do you want to continue?").ask()

    if choice:
        console.print("\n[bold green]Clearing DNS Servers...[/bold green]\n")

        set_dns_servers_to_auto(selected_network)

        console.print("[bold green]DNS Servers Cleared successfully![/bold green]\n")

        display_active_dns()
    else:
        console.print("\n[bold red]Aborting...[/bold red]")


def getting_dns_input() -> Union[Tuple[str], Tuple[str, str]]:
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
