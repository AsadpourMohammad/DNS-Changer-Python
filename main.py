from dns_functions import display_active_dns, setting_dns_servers, getting_dns_input, clearing_dns_servers
from system_utils import is_admin, clear_terminal, press_any_key_to_continue


def display_main_menu() -> None:
    print("""
1. See current Network Connections and DNS Servers
2. Set DNS Servers to Shecan DNS Servers
3. Set DNS Servers to Google DNS Servers
4. Set DNS Servers to specified DNS Servers
5. Clear DNS Servers (Set to Auto)
6. Exit
""")


def handle_see_current_dns_servers() -> None:
    clear_terminal()
    display_active_dns()
    press_any_key_to_continue()


def handle_set_dns_servers(dns_servers: tuple) -> None:
    clear_terminal()
    setting_dns_servers(dns_servers)
    press_any_key_to_continue()


def handle_set_dns_servers_to_specified() -> None:
    dns_servers = getting_dns_input()
    setting_dns_servers(dns_servers)
    press_any_key_to_continue()


def handle_clear_dsn_servers() -> None:
    clear_terminal()
    clearing_dns_servers()
    press_any_key_to_continue()


def main():
    shecan_dns_servers = ("178.22.122.100", "185.51.200.2")
    google_dns_servers = ('8.8.8.8', '8.8.4.4')

    menu_options = {
        "1": handle_see_current_dns_servers,
        "2": lambda: handle_set_dns_servers(shecan_dns_servers),
        "3": lambda: handle_set_dns_servers(google_dns_servers),
        "4": handle_set_dns_servers_to_specified,
        "5": handle_clear_dsn_servers,
        "6": exit
    }

    while True:
        clear_terminal()

        display_active_dns()

        display_main_menu()

        choice = input("> ")
        
        if choice == "6":
            print("Exiting...")
            break

        try:
            menu_options[choice]()
        except KeyError:
            continue


        


if __name__ == '__main__':
    if not is_admin():
        print("""
        Because this script uses WMI module to change your DNS servers,
        you need to run this script as an Administrator, otherwise it will not work.""")

        exit(1)
    else:
        main()
