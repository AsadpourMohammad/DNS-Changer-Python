import ctypes
import msvcrt
import os
import re
import traceback

from questionary import Choice, Style, Separator, select

from rich.console import Console
from rich.panel import Panel

from dns_changer_cli.dns_actions import active_networks_panel, set_dns_servers_panel, input_custom_dns_panel
from dns_changer_cli.json_data import get_saved_dns_providers

console = Console()


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def create_menu_options():
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


def cli():
    menu_options = create_menu_options()

    while True:
        active_networks_panel()

        choice = select("Set DNS Servers to:",
                        choices=menu_options.keys(),
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

        if choice == "Exit" or choice is None:
            console.print("[bold light_cyan3]Exiting...[/bold light_cyan3]")
            break

        menu_options[choice]()

        console.print("\n[bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]")

        if msvcrt.getch():
            clear_terminal()


def main():
    clear_terminal()

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
        panel = Panel(non_windows_err_msg, title="DNS Changer Application", style="bold magenta", width=112)

        console.print(panel)

        if msvcrt.getch():
            return

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            panel = Panel(not_admin_err_msg, title="DNS Changer Application", style="bold magenta", width=112)

            console.print(panel)

            msvcrt.getch()
        else:
            cli()
    except Exception:
        traceback.print_exc()
