import questionary
from rich.console import Console
from rich.panel import Panel
from questionary import Style
import msvcrt

from dns_changer_cli.dns_actions import display_active_dns, setting_dns_servers, getting_dns_input, \
    clearing_dns_servers
from dns_changer_cli.system_utils import is_admin, clear_terminal, press_any_key_to_continue, \
    get_dns_addresses_for_provider

console = Console()


def handle_see_current_dns_servers() -> None:
    clear_terminal()
    display_active_dns()
    press_any_key_to_continue()


def handle_set_dns_servers(dns_servers: tuple) -> None:
    setting_dns_servers(dns_servers)
    press_any_key_to_continue()


def handle_set_dns_servers_to_specified() -> None:
    dns_servers = getting_dns_input()
    setting_dns_servers(dns_servers)
    press_any_key_to_continue()


def handle_clear_dns_servers() -> None:
    clearing_dns_servers()
    press_any_key_to_continue()


def cli():
    menu_options = {
        "Set DNS servers to Shecan": lambda: handle_set_dns_servers(get_dns_addresses_for_provider("Shecan")),
        "Set DNS servers to Google": lambda: handle_set_dns_servers(get_dns_addresses_for_provider("Google")),
        "Set DNS servers to specified": handle_set_dns_servers_to_specified,
        "Clear DNS servers": handle_clear_dns_servers,
    }

    while True:
        clear_terminal()

        display_active_dns()

        choice = questionary.select("DNS Changer Application",
                                    choices=[
                                        "Set DNS servers to Shecan",
                                        "Set DNS servers to Google",
                                        "Set DNS servers to specified",
                                        "Clear DNS servers",
                                        "Exit"
                                    ],
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

        menu_options[choice]()


def main():
    if not is_admin():
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
