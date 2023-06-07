from typing import Literal

from questionary import confirm

from dns_changer import (
    TableWrapper, TablePanelWrapper, print_panel, print_text, print_err,
    get_provider_of_servers, get_provider_and_servers_of_network_dns,
)
from .panel_active_networks import active_networks_panel
from .panel_select_network import select_network_panel
from ...dns.utils.dns_windows_utils import set_dns_of_network


def abort():
    print_err("Aborting...")


def set_dns_servers_panel(action: Literal["change", "clear"], new_servers: tuple[str, str] = None) -> None:
    if action == "change" and not new_servers:
        abort()
        return

    selected_network = select_network_panel()

    if not selected_network:
        abort()
        return

    old_provider, old_servers = get_provider_and_servers_of_network_dns(selected_network).values()

    new_provider = get_provider_of_servers(new_servers) if action == "change" else "Auto"

    if (action == "change" and old_servers == new_servers) or (action == "clear" and old_provider == "Auto"):
        print_err(f"Your DNS Servers are already set to {new_servers if action == 'change' else 'Auto'}'.")
        return

    choice = _confirm_dns_change_panel(old_provider, old_servers, new_provider, new_servers)

    if not choice:
        abort()
        return

    def action_function():
        return set_dns_of_network(action, selected_network, new_servers)

    _handle_dns_action(action, action_function)


def _confirm_dns_change_panel(current_name: str, current_servers: tuple[str, str],
                              new_name: str, new_servers: tuple[str, str]) -> bool:
    new_line = "\n"

    change_info = [
        f"{new_line}".join(current_servers),
        current_name,
        f"{new_line}".join(new_servers) if new_servers else "Unknown",
        new_name
    ]

    table_wrapper = TableWrapper(
        title="Confirm DNS Servers Change",
        columns=["Current DNS Servers", "Current Provider", "New DNS Servers", "New Provider"],
        rows=change_info,
        type="show-diff"
    )

    panel_wrapper = TablePanelWrapper(table=table_wrapper.table)

    print_panel(panel_wrapper.panel)

    return confirm("Are you sure you want to change the DNS Servers?").ask()


def _handle_dns_action(action: Literal["change", "clear"], action_function: set_dns_of_network) -> None:
    print_text(f"\n{'Changing' if action == 'change' else 'Clearing'} DNS Servers..\n")

    if action_function():
        print_text(f"DNS Servers {'changed' if action == 'change' else 'cleared'} successfully!\n")

        active_networks_panel()
    else:
        print_err(f"An error occurred while trying to {action} the DNS Servers! Aborting...\n")
