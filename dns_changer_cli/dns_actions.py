from typing import Union, Tuple

import questionary
from questionary import Style

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns

from dns_utils.dns_utils import get_dns_servers, set_dns_servers, set_dns_servers_to_auto, is_dns_auto_obtain
from dns_changer_cli.system_utils import get_all_dns_addresses, is_dns_server_valid

console = Console()


def confirm_dns_servers_change(current_name: str, current_servers: tuple[str],
                               new_name: str, new_servers: tuple[str]) -> bool:
    table = Table(title="Confirm DNS Servers Change", box=box.ROUNDED, show_lines=True, width=100)

    table.add_column("Current DNS Servers", style="cyan bold", header_style="light_sky_blue1")
    table.add_column("Current Provider", style="yellow3 bold", header_style="light_sky_blue1")
    table.add_column("New DNS Servers", style="red3 bold", header_style="light_sky_blue1")
    table.add_column("New Provider", style="yellow3 bold", header_style="light_sky_blue1")

    new_line = '\n'
    table.add_row(f"{new_line}".join(current_servers), current_name,
                  f"{new_line}".join(new_servers) if new_servers else "Unknown", new_name)

    panel = Panel(renderable=table, title="DNS Changer Application",
                  style="bold", title_align="left", border_style="cyan bold", padding=(1, 5))

    console.print(Columns([panel], align="center"))

    return questionary.confirm("Are you sure you want to change the DNS Servers?").ask()


def handle_user_choice(choice: str, action: str,
                       action_function: Union[set_dns_servers, set_dns_servers_to_auto]) -> bool:
    if choice:
        console.print(f"\n[bold green]{'Changing' if action == 'change' else 'Clearing'} DNS Servers...[/bold green]\n")

        if action_function():
            console.print(
                f"[bold green]DNS Servers {'changed' if action == 'change' else 'cleared'} successfully![/bold green]\n")

            display_active_dns()
        else:
            console.print(
                f"[bold red]An error occurred while trying to {action} the DNS Servers! Aborting...[/bold red]\n")

        return True
    else:
        console.print("\n[bold red]Aborting...[/bold red]")
        return False


def get_network_and_servers() -> list[tuple[str, tuple[str]]]:
    current_dns_servers = get_dns_servers()
    network_and_servers = []

    for network_connection in current_dns_servers:
        dns_servers = current_dns_servers[network_connection]
        network_and_servers.append((network_connection, dns_servers))

    return network_and_servers


def get_network():
    network_and_servers = get_network_and_servers()

    if not network_and_servers:
        console.print("[bold red]No active network connections found![/bold red]\n")
        return None

    selected_network = select_network_connection(network_and_servers)

    if not selected_network:
        console.print("[bold red]Aborting...[/bold red]\n")
        return None

    return selected_network


def get_network_name_and_server(network):
    servers = get_dns_servers()[network]

    name = "Auto" if is_dns_auto_obtain(network) else get_server_name(servers)

    return name, servers


def get_server_name(servers: tuple[str]) -> str:
    return next((dns_name for dns_name, dns_servers in get_all_dns_addresses().items() if dns_servers == servers),
                "Unknown")


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

    table = Table(title="Current DNS Information", box=box.ROUNDED, show_lines=True, width=100)

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


def getting_dns_input() -> Union[Tuple[str], Tuple[str, str]]:
    def get_dns(placement):
        return questionary.text(f"{placement} DNS Server:",
                                validate=lambda text: True if is_dns_server_valid(
                                    text) else "Invalid IP Address.").ask()

    primary_dns = get_dns("Primary")
    secondary_dns = get_dns("Secondary")

    return primary_dns, secondary_dns


def setting_dns_servers(action: str, new_servers: tuple[str] = None) -> None:
    selected_network = get_network()

    if not selected_network:
        return

    current_server_name, current_servers = get_network_name_and_server(selected_network)

    new_servers_name = get_server_name(new_servers) if action == "change" else "Auto"

    if current_server_name == new_servers_name:
        console.print(f"\n[bold red]Your DNS Servers are already set to '{new_servers_name}'.[/bold red]")
        return

    choice = confirm_dns_servers_change(current_server_name, current_servers, new_servers_name,
                                        new_servers)

    def change_dns():
        return set_dns_servers(selected_network, new_servers)

    def clear_dns():
        return set_dns_servers_to_auto(selected_network)

    action_function = change_dns if action == "change" else clear_dns

    handle_user_choice(choice, action, action_function)
