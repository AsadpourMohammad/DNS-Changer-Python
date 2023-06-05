import re
from typing import Union, Tuple

import questionary
from questionary import Style

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns

from dns_utils.dns_windows_utils import get_all_networks_and_dns_servers, set_dns_of_network, is_network_dns_auto
from dns_changer_cli.json_data import get_saved_dns_providers

console = Console()


def abort():
    console.print("[bold red]Aborting...[/bold red]")


def active_networks_panel() -> None:
    networks_and_servers = get_all_networks_and_dns_servers()

    table = Table(title="Current DNS Information", box=box.ROUNDED, show_lines=True, width=100)

    table.add_column("Network Connection", style="cyan bold", header_style="light_sky_blue1")
    table.add_column("DNS Servers", style="red3 bold", header_style="light_sky_blue1")
    table.add_column("Provider", style="yellow3 bold", header_style="light_sky_blue1")

    for network, dns_servers in networks_and_servers.items():
        provider = get_provider_and_servers_of_network_dns(network)['provider']

        table.add_row(network, ", ".join(dns_servers), provider)

    panel = Panel(renderable=table, title="DNS Changer Application", style="bold", title_align="left",
                  border_style="cyan bold", padding=(1, 5))

    console.print(Columns([panel], align="center"))


def setting_dns_servers(action: str, new_servers: tuple[str] = None) -> None:
    if action == "change" and not new_servers:
        abort()
        return

    selected_network = get_user_select_network()

    if not selected_network:
        abort()
        return

    old_provider, old_servers = get_provider_and_servers_of_network_dns(selected_network).values()

    new_provider = get_provider_of_servers(new_servers) if action == "change" else "Auto"

    if (action == "change" and old_servers == new_servers) or (action == "clear" and old_provider == "Auto"):
        console.print(f"\n[bold red]Your DNS Servers are already set to "
                      f"'{new_servers if action == 'change' else 'Auto'}'.[/bold red]")
        return

    choice = confirm_dns_change_panel(old_provider, old_servers, new_provider, new_servers)

    if not choice:
        abort()
        return

    action_function = lambda: set_dns_of_network(action, selected_network, new_servers)

    handle_dns_action(action, action_function)


def input_custom_dns_panel() -> Union[Tuple[str], Tuple[str, str], None]:
    def is_dns_server_valid(ip_address: str) -> bool:
        return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_address))

    def get_dns(placement) -> str:
        return questionary.text(f"{placement} DNS Server:",
                                validate=lambda text: True if is_dns_server_valid(text)
                                else "Invalid IP Address.").ask()

    primary_dns = get_dns("Primary")

    if not primary_dns:
        return None

    secondary_dns = get_dns("Secondary")

    if not secondary_dns:
        return None

    return primary_dns, secondary_dns


def confirm_dns_change_panel(current_name: str, current_servers: tuple[str], new_name: str,
                             new_servers: tuple[str]) -> bool:
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


def handle_dns_action(action: str, action_function: set_dns_of_network) -> None:
    console.print(f"\n[bold green]{'Changing' if action == 'change' else 'Clearing'} DNS Servers...[/bold green]\n")

    if action_function():
        console.print(
            f"[bold green]DNS Servers {'changed' if action == 'change' else 'cleared'} successfully![/bold green]\n")

        active_networks_panel()
    else:
        console.print(
            f"[bold red]An error occurred while trying to {action} the DNS Servers! Aborting...[/bold red]\n")


def get_user_select_network():
    network_and_servers = get_all_networks_and_dns_servers()

    if not network_and_servers:
        console.print("[bold red]No active network connections found![/bold red]\n")
        return None

    selected_network = select_network_connection_panel(network_and_servers)

    if not selected_network:
        return None

    return selected_network


def select_network_connection_panel(networks_and_servers):
    network_choices = [network_connection for network_connection in networks_and_servers.keys()]

    selected_network = questionary.select("Select the network connection:", choices=network_choices, instruction=" ",
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


def get_provider_and_servers_of_network_dns(network: str) -> dict[str, any]:
    """
    Checks to see if the DNS Servers of the selected network match a known provider.
    It can either be a known provider, "Auto" if network is set to auto obtain, or "Unknown" if no match is made.
    """
    servers = get_all_networks_and_dns_servers()[network]

    provider = "Auto" if is_network_dns_auto(network) else get_provider_of_servers(servers)

    return {'provider': provider, 'servers': servers}


def get_provider_of_servers(servers: tuple[str]) -> str:
    return next((provider for provider, dns_servers in get_saved_dns_providers().items() if dns_servers == servers),
                "Unknown")
