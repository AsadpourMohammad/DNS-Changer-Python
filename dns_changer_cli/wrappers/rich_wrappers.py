from typing import List, Literal

from rich.table import Table
from rich import box
from rich.panel import Panel

class TextPanelWrapper():
    def __init__(self, title: str, text: str):
        self.title = title
        self.panel = Panel(renderable=text, title=title, style="bold magenta", width=112)


class TablePanelWrapper():
    def __init__(self, title: str, table: Table):
        self.title = title
        self.panel = Panel(renderable=table, title=title, style="bold", title_align="left",
                           border_style="cyan bold", padding=(1, 5))


class TableWrapper():
    def __init__(self, title: str, columns: List, rows: List, type: Literal["show-current", "show-diff"]):
        self.title = title
        self.table = Table(title=title, box=box.ROUNDED, show_lines=True, width=100)
        self.add_columns(columns)
        self.add_rows(rows, type)

    
    def add_columns(self, columns: List):
        for column in columns:
            self.table.add_column(column, style="cyan bold", header_style="light_sky_blue1")
    
    def add_rows(self, rows: List, type: str):
        if type == "show-current":
            for network, servers, provider in rows:
                self.table.add_row(network, servers, provider, style="bright_red bold")
        elif type == "show-diff":
            old_provider, old_servers, new_provider, new_servers = rows
            self.table.add_row(old_provider, old_servers, new_provider, new_servers, style="bright_red bold")
