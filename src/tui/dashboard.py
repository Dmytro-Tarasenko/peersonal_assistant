"""
Dashboard widget
"""
from rich.console import RenderableType
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Label, Input, Button
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

    def on_show(self) -> None:
        app = self.app
        abook_len = len(app.address_book.data)
        yield Label("AddressBook is loaded", classes="db_stats_title")
        yield Label(f"contains {abook_len} items", classes="db_stats_nums")
        self.refresh()


class NoteBookStats(Widget):
    """
    Widget to display statistic of AddressBook and NoteBook
    """
    def compose(self) -> ComposeResult:
        app = self.app
        nbook_len = len(app.note_book.data)
        yield Label("Notebook is loaded", classes="db_stats_title")
        yield Label(f"contains {nbook_len} items", classes="db_stats_nums")

    def on_show(self) -> ComposeResult:
        app = self.app
        nbook_len = len(app.note_book.data)
        yield Label("Notebook is loaded", classes="db_stats_title")
        yield Label(f"contains {nbook_len} items", classes="db_stats_nums")
        self.refresh()


class TodaysMates(Static):
    """
    Displays today`s Birthday mates
    """
    today_mates = []
    def on_mount(self) -> None:
        self.styles.border = ("round", "#FFD900")

    def render(self) -> RenderableType:
        self.today_mates = self.app.address_book.today_mates()
        table = Table(title="Today birthday mates")
        table.box = None
        table.add_column("#", justify="center", width=6)
        table.add_column("Name", justify="left", width=20)
        table.add_column("Age", justify="center", width=6)
        num_line = 1
        for mate in self.today_mates:
            cur_year = datetime.today().year
            born_year = int(mate.birthday[-4:])
            age = str(cur_year - born_year)
            table.add_row(str(num_line), mate.name, age)
            num_line += 1

        return table


class UpcomingMates(Widget):
    """Displays upcoming Birthday mates"""
    days_to_watch = 5
    upcoming_mates = []

    def on_mount(self) -> None:
        self.styles.border = ("round", "#FFD900")

    def render(self) -> RenderableType:
        self.upcoming_mates = (self.app.address_book
                               .upcoming_mates(self.days_to_watch))
        title = f"Birthday mates upcoming in {self.days_to_watch}"
        table = Table(title=title)
        table.box = None
        table.add_column("#", justify="center", width=6)
        table.add_column("Name", justify="left", width=20)
        table.add_column("Birthday", justify="center", width=18)
        table.add_column("Age", justify="center", width=6)
        num_line = 1
        for mate in self.upcoming_mates:
            cur_year = datetime.today().year
            born_year = int(mate.birthday[-4:])
            age = str(cur_year - born_year)
            table.add_row(str(num_line),
                          mate.name,
                          mate.birthday,
                          age)
            num_line += 1

        return table


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
                Vertical(
                    Label("Set num. of days to watch for mates:"),
                    Input(placeholder="digits only",
                          restrict=r"\d+",
                          id="db_input_days_to_mates"),
                    Button(label='Set',
                           variant="primary",
                           id="db_set_days")
                ),
                id="db_stats"
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "db_set_days":
                input: Input = self.query_one("#db_input_days_to_mates")
                if not input.value:
                    return
                up_mates: UpcomingMates = self.query_one(UpcomingMates)
                up_mates.days_to_watch = int(input.value)
                up_mates.refresh()
