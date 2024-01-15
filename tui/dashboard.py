"""
Dashboard widget
"""
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Markdown, Static, Label, DataTable
from datetime import datetime


class DateClock(Widget):
    """
    Date Clock widget for Dashboard
    """
    date_str = datetime.today().date().strftime("%A, %d %B %Y")
    cur_time_str = reactive(datetime.today()
                            .time().strftime("%H:%M:%S"))

    def update_time(self) -> None:
        """Update cur_time_str"""
        self.cur_time_str = datetime.today().time().strftime("%H:%M:%S")

    def on_mount(self) -> None:
        """Updating time each second"""
        self.set_interval(1, self.update_time)

    def render(self) -> RenderableType:
        """Render result"""
        render_str = f"{'Today':^26}\n\n"
        render_str += f"{self.date_str}\n{self.cur_time_str:^26}"
        return render_str


class AddressBookStats(Widget):
    """
    Widget to display statistic of AddressBook and NoteBook
    """
    def compose(self) -> ComposeResult:
        app = self.app
        abook_len = len(app.address_book.data)
        yield Label("AddressBook is loaded", classes="db_stats_title")
        yield Label(f"contains {abook_len} items", classes="db_stats_nums")


class NoteBookStats(Widget):
    """
    Widget to display statistic of AddressBook and NoteBook
    """
    def compose(self) -> ComposeResult:
        yield Label("Notebook is loaded", classes="db_stats_title")
        yield Label("contains 12 items", classes="db_stats_nums")


class TodaysMates(Widget):
    """
    Displays today`s Birthday mates
    """
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cell_padding = 2
        table.cursor_type = "row"
        table.add_columns("#", "Name", "Age")
        table.add_row("1", "Engelgardt asdasd", "43")
        table.add_row("2", "Shevchenko", "55")
        table.add_row("3", "Engelgardt", "98")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Today`s Birthday mate(s):"),
            DataTable(classes="data_table")
        )


class UpcomingMates(Widget):
    """Displays upcoming Birthday mates"""

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Upcoming Birthday mate(s) in 5 days:"),
            DataTable(classes="data_table")
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cell_padding = 2
        table.cursor_type = "row"
        table.add_columns("#", "Name", "Birthday", "Age")
        table.add_row("1", "Engelgardt asdasd asdasdasdasdasdasdasdasd", "12-01-1980", "43")
        table.add_row("2", "Shevchenko", "16-01-1969", "55")
        table.add_row("3", "Engelgardt", "17-01-1926", "98")


class DashBoard(Static):
    """
    Main layout of Dashboard
    """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                TodaysMates(id="db_bd_today"),
                UpcomingMates(id="db_bd_upcoming"),
                id="db_bday"
            ),
            Vertical(
                DateClock(classes="db_stats_row"),
                AddressBookStats(classes="db_stats_row"),
                NoteBookStats(classes="db_stats_row"),
                id="db_stats"
            )
        )
