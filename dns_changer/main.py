import ctypes
import msvcrt
import os
import traceback

from . import TextPanelWrapper, print_panel
from .cli.main_panel import main_menu


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_terminal()

    non_windows_os_err_msg = """
    Currently, this app can only be run on Windows, and won't work on other operating systems.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    not_admin_err_msg = """
    Because this script changes your DNS server addresses, 
    you need to run this Python program as an Administrator, otherwise it will not work properly.

    [bold light_steel_blue1]Press any key to continue...[/bold light_steel_blue1]
    """

    if os.name != "nt":
        panel_wrapper = TextPanelWrapper(text=non_windows_os_err_msg)

        print_panel(panel_wrapper.panel)

        if msvcrt.getch():
            return

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            panel_wrapper = TextPanelWrapper(text=not_admin_err_msg)

            print_panel(panel_wrapper.panel)

            msvcrt.getch()
        else:
            main_menu()
    except Exception:
        traceback.print_exc()
