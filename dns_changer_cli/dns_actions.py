import re
from typing import Union, Tuple, Literal

from questionary import Style, text, confirm, select

from rich.console import Console
from rich.columns import Columns

from dns_changer_cli.wrappers.rich_wrappers import TablePanelWrapper, TableWrapper
from dns_utils.dns_windows_utils import get_all_networks_and_dns_servers, set_dns_of_network
from dns_changer_cli.dns_provider import get_provider_and_servers_of_network_dns, get_provider_of_servers

__console__ = Console()


def active_networks_panel() -> None:
    networks_and_servers = get_all_networks_and_dns_servers()

    all_networks_info = [
        [network, ", ".join(dns_servers), get_provider_of_servers(dns_servers)]
        for network, dns_servers in networks_and_servers.items()
    ]

    table_wrapper = TableWrapper(title="Current DNS Information",
                                 columns=["Network Connection", "DNS Servers", "Provider"],
                                 rows=all_networks_info,
                                 type="show-current")

    panel_wrapper = TablePanelWrapper(title=table_wrapper.title, table=table_wrapper.table)

    __console__.print(Columns([panel_wrapper.panel], align="center"))


def input_custom_dns_panel() -> Union[Tuple[str], Tuple[str, str], None]:
    def is_dns_server_valid(ip_address: str) -> bool:
        return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_address))

    def get_dns(placement) -> str:
        return text(f"{placement} DNS Server:",
                    validate=lambda input_dns: True if is_dns_server_valid(input_dns)
                    else "Invalid IP Address.").ask()

    primary_dns = get_dns("Primary")

    if not primary_dns:
        return None

    secondary_dns = get_dns("Secondary")

    if not secondary_dns:
        return None

    return primary_dns, secondary_dns


def set_dns_servers_panel(action: Literal["change", "clear"], new_servers: tuple[str] = None) -> None:
    if action == "change" and not new_servers:
        __abort__()
        return

    selected_network = __get_user_select_network__()

    if not selected_network:
        __abort__()
        return

    old_provider, old_servers = get_provider_and_servers_of_network_dns(selected_network).values()

    new_provider = get_provider_of_servers(new_servers) if action == "change" else "Auto"

    if (action == "change" and old_servers == new_servers) or (action == "clear" and old_provider == "Auto"):
        __console__.print(f"\n[bold red]Your DNS Servers are already set to "
                          f"'{new_servers if action == 'change' else 'Auto'}'.[/bold red]")
        return

    choice = __confirm_dns_change_panel__(old_provider, old_servers, new_provider, new_servers)

    if not choice:
        __abort__()
        return

    def action_function():
        return set_dns_of_network(action, selected_network, new_servers)

    __handle_dns_action__(action, action_function)


def __get_user_select_network__():
    network_and_servers = get_all_networks_and_dns_servers()

    if not network_and_servers:
        __console__.print("[bold red]No active network connections found![/bold red]\n")
        return None

    selected_network = __select_network_connection_panel__(network_and_servers)

    if not selected_network:
        return None

    return selected_network


def __select_network_connection_panel__(networks_and_servers):
    network_choices = [network_connection for network_connection in networks_and_servers.keys()]

    selected_network = select("Select the network connection:", choices=network_choices, instruction=" ",
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


def __confirm_dns_change_panel__(current_name: str, current_servers: tuple[str],
                                 new_name: str, new_servers: tuple[str]) -> bool:
    new_line = "\n"

    change_info = [
        f"{new_line}".join(current_servers), current_name,
        f"{new_line}".join(new_servers) if new_servers else "Unknown", new_name
    ]

    table_wrapper = TableWrapper(title="Confirm DNS Servers Change",
                                 columns=["Current DNS Servers", "Current Provider", "New DNS Servers", "New Provider"],
                                 rows=change_info,
                                 type="show-diff")

    panel_wrapper = TablePanelWrapper(title=table_wrapper.title, table=table_wrapper.table)

    __console__.print(Columns([panel_wrapper.panel], align="center"))

    return confirm("Are you sure you want to change the DNS Servers?").ask()


def __handle_dns_action__(action: Literal["change", "clear"], action_function: set_dns_of_network) -> None:
    __console__.print(f"\n[bold green]{'Changing' if action == 'change' else 'Clearing'} DNS Servers...[/bold green]\n")

    if action_function():
        __console__.print(
            f"[bold green]DNS Servers {'changed' if action == 'change' else 'cleared'} successfully![/bold green]\n")

        active_networks_panel()
    else:
        __console__.print(
            f"[bold red]An error occurred while trying to {action} the DNS Servers! Aborting...[/bold red]\n")


def __abort__():
    __console__.print("[bold red]Aborting...[/bold red]")
