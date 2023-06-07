import msvcrt
import os
import re

from questionary import Choice, Separator

from .. import SelectWrapper, print_text
from .sub_panels.panel_active_networks import active_networks_panel
from .sub_panels.panel_change_dns import set_dns_servers_panel
from .sub_panels.panel_custom_dns import custom_dns_panel
from ..dns.data.json_utils import get_saved_providers


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    while True:
        active_networks_panel()

        menu_options = _create_menu_options()

        choice = SelectWrapper("Set DNS Servers to:", choices=menu_options.keys())()

        if choice == "Exit" or choice is None:
            print_text("Exiting...")
            break

        menu_options[choice]()

        print_text("\nPress any key to continue...")

        if msvcrt.getch():
            clear_terminal()


def _create_menu_options():
    def is_dns_server_valid(ip_address: str) -> bool:
        return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_address))

    providers_and_servers = get_saved_providers()

    menu_options = {}

    for provider, dns_servers in providers_and_servers.items():
        if all(is_dns_server_valid(server) for server in dns_servers):
            menu_options[provider] = lambda servers=dns_servers: set_dns_servers_panel("change", servers)
        else:
            invalid_choice = Choice(provider, disabled="Invalid DNS Servers")
            menu_options[invalid_choice] = None

    menu_options["Custom"] = lambda: set_dns_servers_panel("change", custom_dns_panel())
    menu_options["Auto"] = lambda: set_dns_servers_panel("clear")

    separator = Separator()
    menu_options[separator] = None

    menu_options["Exit"] = None

    return menu_options
