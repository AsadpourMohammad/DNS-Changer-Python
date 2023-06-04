import questionary
from questionary import Choice
from questionary import Style

from rich.console import Console
from rich.panel import Panel

import ctypes
import msvcrt
import os

from dns_changer_cli.dns_actions import display_active_dns, setting_dns_servers, getting_dns_input
from dns_changer_cli.system_utils import clear_terminal, get_all_dns_addresses, is_dns_server_valid

console = Console()


def create_menu():
    networks_and_servers = get_all_dns_addresses()

    menu_options = {}

    for network, dns_servers in networks_and_servers.items():
        if all(is_dns_server_valid(server) for server in dns_servers):
            menu_options[network] = lambda servers=dns_servers: setting_dns_servers("change", servers)
        else:
            invalid_choice = Choice(network, disabled="Invalid DNS Servers")
            menu_options[invalid_choice] = None

    menu_options["Custom"] = lambda: setting_dns_servers("change", getting_dns_input())
    menu_options["Auto"] = lambda: setting_dns_servers("clear")
    menu_options["Exit"] = None

    return menu_options


def cli():
    menu = create_menu()

    while True:
        display_active_dns()

        choice = questionary.select("Set DNS Servers to:",
                                    choices=menu.keys(),
                                    style=Style(
                                        [
                                            ("qmark", "fg:#673ab7 bold"),
                                            ('highlighted', 'fg:#d70000 bold'),
                                            ("pointer", "fg:#d70000 bold"),
                                            ('text', 'fg:#d7ffff bold'),
                                            ("answer", "fg:#afd7ff bold"),
                                        ]
                                    )).ask()

        if choice == "Exit":
            console.print("[bold light_cyan3]Exiting...[/bold light_cyan3]")
            break

        menu[choice]()

        console.print("\n[bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]")

        if msvcrt.getch():
            clear_terminal()


def main():
    clear_terminal()

    if os.name != "nt":
        panel = Panel("""
        This application can only be run on Windows, and won't work on other operating systems.

        [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
        """, title="DNS Changer Application", style="bold magenta", width=112)

        console.print(panel)

        if msvcrt.getch():
            return

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            panel = Panel("""
    Because this script changes your DNS servers, 
    you need to run this script as an Administrator, otherwise it will not work.

    Also, please note that this application can only been run on Windows.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """, title="DNS Changer Application", style="bold magenta")

            console.print(panel)

            msvcrt.getch()
        else:
            cli()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
