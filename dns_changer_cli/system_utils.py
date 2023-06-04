import ctypes
import msvcrt
import os
from rich.console import Console

console = Console()


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def press_any_key_to_continue() -> None:
    console.print("\n[bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]")
    msvcrt.getch()


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def get_all_dns_addresses():
    dns_addresses = {
        "Shecan": ("178.22.122.100", "185.51.200.2"),
        "Google": ("8.8.8.8", "8.8.4.4")
    }

    return dns_addresses


def get_dns_addresses_for_provider(provider_name):
    if provider_name in get_all_dns_addresses():
        return get_all_dns_addresses()[provider_name]
    else:
        raise ValueError("Invalid DNS provider name")