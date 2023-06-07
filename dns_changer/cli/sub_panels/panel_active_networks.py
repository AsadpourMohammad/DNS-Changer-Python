from dns_changer import (
    TableWrapper, TablePanelWrapper, print_panel,
    get_provider_and_servers_of_network_dns, get_all_networks_and_dns_servers
)


def active_networks_panel() -> None:
    networks_and_servers = get_all_networks_and_dns_servers()

    all_networks_info = [
        [network, ", ".join(dns_servers), get_provider_and_servers_of_network_dns(network)['provider']]
        for network, dns_servers in networks_and_servers.items()
    ]

    table_wrapper = TableWrapper(title="Current DNS Information",
                                 columns=["Network Connection", "DNS Servers", "Provider"],
                                 rows=all_networks_info,
                                 type="show-current")

    panel_wrapper = TablePanelWrapper(table=table_wrapper.table)

    print_panel(panel_wrapper.panel)
