from dns_changer import get_all_networks_and_dns_servers, SelectWrapper, print_err


def select_network_panel():
    networks_and_servers = get_all_networks_and_dns_servers()

    if not networks_and_servers:
        print_err("No active network connections found!\n")
        return None

    network_choices = [network for network in networks_and_servers.keys()]

    selected_network = SelectWrapper(question="Select the network connection:", choices=network_choices)()

    if not selected_network:
        return None

    return selected_network
