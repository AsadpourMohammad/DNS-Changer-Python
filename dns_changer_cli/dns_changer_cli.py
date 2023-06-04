import ctypes
import msvcrt
import os
import re
import traceback

import questionary
from questionary import Choice, Style, Separator

from rich.console import Console
from rich.panel import Panel

from dns_changer_cli.dns_actions import display_active_dns, setting_dns_servers, input_custom_dns
from dns_changer_cli.json_data import get_all_dns_addresses

console = Console()


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def create_menu():
    def is_dns_server_valid(ip_address: str) -> bool:
        return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_address))

    networks_and_servers = get_all_dns_addresses()

    menu_options = {}

    for network, dns_servers in networks_and_servers.items():
        if all(is_dns_server_valid(server) for server in dns_servers):
            menu_options[network] = lambda servers=dns_servers: setting_dns_servers("change", servers)
        else:
            invalid_choice = Choice(network, disabled="Invalid DNS Servers")
            menu_options[invalid_choice] = None

    menu_options["Custom"] = lambda: setting_dns_servers("change", input_custom_dns())
    menu_options["Auto"] = lambda: setting_dns_servers("clear")

    separator = Separator()
    menu_options[separator] = None

    menu_options["Exit"] = None

    return menu_options


def cli():
    menu = create_menu()

    while True:
        display_active_dns()

        choice = questionary.select("Set DNS Servers to:",
                                    choices=menu.keys(),
                                    instruction=" ",
                                    style=Style(
                                        [
                                            ("qmark", "fg:#673ab7 bold"),
                                            ('highlighted', 'fg:#d70000 bold'),
                                            ("pointer", "fg:#d70000 bold"),
                                            ('text', 'fg:#d7ffff bold'),
                                            ("answer", "fg:#afd7ff bold"),
                                        ]
                                    )).ask()

        if choice is None:
            console.print("[bold light_cyan3]Aborting...[/bold light_cyan3]")
            break

        if choice == "Exit":
            console.print("[bold light_cyan3]Exiting...[/bold light_cyan3]")
            break

        menu[choice]()

        console.print("\n[bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]")

        if msvcrt.getch():
            clear_terminal()


def main():
    clear_terminal()

    os_message = """
    Currently, this app can only be run on Windows, and won't work on other operating systems.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    user_message = """
    Because this script changes your DNS server addresses, 
    you need to run this Python program as an Administrator, otherwise it will not work properly.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    if os.name != "nt":
        panel = Panel(os_message, title="DNS Changer Application", style="bold magenta", width=112)

        console.print(panel)

        if msvcrt.getch():
            return

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            panel = Panel(user_message, title="DNS Changer Application", style="bold magenta", width=112)

            console.print(panel)

            msvcrt.getch()
        else:
            cli()
    except Exception:
        traceback.print_exc()
