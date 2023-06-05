import ctypes
import msvcrt
import os
import re
import traceback

from questionary import Choice, Separator

from rich.console import Console

from dns_changer_cli.wrappers.rich_wrappers import TextPanelWrapper
from dns_changer_cli.wrappers.questionary_wrappers import SelectWrapper
from dns_changer_cli.dns_actions import active_networks_panel, set_dns_servers_panel, input_custom_dns_panel
from dns_changer_cli.dns_provider import get_saved_dns_providers

__console__ = Console()


def __clear_terminal__() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def __create_menu_options__():
    def is_dns_server_valid(ip_address: str) -> bool:
        return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_address))

    providers_and_servers = get_saved_dns_providers()

    menu_options = {}

    for provider, dns_servers in providers_and_servers.items():
        if all(is_dns_server_valid(server) for server in dns_servers):
            menu_options[provider] = lambda servers=dns_servers: set_dns_servers_panel("change", servers)
        else:
            invalid_choice = Choice(provider, disabled="Invalid DNS Servers")
            menu_options[invalid_choice] = None

    menu_options["Custom"] = lambda: set_dns_servers_panel("change", input_custom_dns_panel())
    menu_options["Auto"] = lambda: set_dns_servers_panel("clear")

    separator = Separator()
    menu_options[separator] = None

    menu_options["Exit"] = None

    return menu_options


def __cli__():
    menu_options = __create_menu_options__()

    while True:
        active_networks_panel()

        choice = SelectWrapper("Set DNS Servers to:", choices=menu_options.keys())()

        if choice == "Exit" or choice is None:
            __console__.print("[bold light_cyan3]Exiting...[/bold light_cyan3]")
            break

        menu_options[choice]()

        __console__.print("\n[bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]")

        if msvcrt.getch():
            __clear_terminal__()


def main():
    __clear_terminal__()

    non_windows_err_msg = """
    Currently, this app can only be run on Windows, and won't work on other operating systems.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    not_admin_err_msg = """
    Because this script changes your DNS server addresses, 
    you need to run this Python program as an Administrator, otherwise it will not work properly.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    if os.name != "nt":
        panel_wrapper = TextPanelWrapper("DNS Changer Application", non_windows_err_msg)

        __console__.print(panel_wrapper.panel)

        if msvcrt.getch():
            return

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            panel_wrapper = TextPanelWrapper("DNS Changer Application", not_admin_err_msg)

            __console__.print(panel_wrapper.panel)

            msvcrt.getch()
        else:
            __cli__()
    except Exception:
        traceback.print_exc()
