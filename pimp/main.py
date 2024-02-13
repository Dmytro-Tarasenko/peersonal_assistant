"""
Personal_assistant is a personal information manager for everyday tasks:
    keeping contacts - names, addresses, phone etc.;
    remaindering of upcoming birthdays;
    keeping personal notes
"""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (Header,
                             Footer,
                             TabbedContent,
                             TabPane)

from cls.NoteBook import Notebook
from cls.AddressBook import AddressBook
from cls.PimpConfig import PimpConfig
from tui import contacts, sorter, notes, settings, dashboard
import pickle


class PersonalAssistant(App):
    """
    Main clas for personal_assistant textual app
    """

    BINDINGS = [
        ("d", "show_tab('dashbrd')", "Dashboard"),
        ("c", "show_tab('contacts')", "Contacts"),
        ("n", "show_tab('notes')", "Notes"),
        ("f", "show_tab('sort')", "File sorter"),
        ("a", "show_tab('about')", "About"),
        Binding("ctrl+c", "quit", "Save all and quit",
                show=True, priority=True)
    ]

    CSS_PATH = ["tcss/main.tcss",
                "tcss/dashboard.tcss",
                "tcss/sorter.tcss",
                "tcss/notes.tcss",
                "tcss/contacts.tcss"]

    def __init__(
            self,
            driver_class=None,
            css_path=None,
            watch_css: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.address_book = None
        self.note_book = None
        self.config = PimpConfig()

    def compose(self) -> ComposeResult:
        """Create children for the application"""
        self.config.read_config("config.yaml")
        self.address_book: AddressBook = self.config.address_book
        self.note_book: Notebook = self.config.note_book

        yield Header()
        yield Footer()

        with TabbedContent():
            with TabPane("Dashboard", id="dashbrd"):
                yield dashboard.DashBoard()
            with TabPane("Contacts", id="contacts"):
                yield contacts.Contacts()
            with TabPane("Notes", id="notes"):
                yield notes.Notes()
            with TabPane("File Sorter", id="sort"):
                yield sorter.Sorter()
            with TabPane("About", id="about"):
                yield settings.paSettings

    def action_show_tab(self, tab_id: str) -> None:
        """
        Switching tabs by id
        :param tab_id: identifier for tab user clicked or entered command
        :return: None
        """
        self.get_child_by_type(TabbedContent).active = tab_id

    def action_quit(self) -> None:
        """Performs quit action"""
        with open("data/addressbook.bin", "wb") as ab_file:
            pickle.dump(self.address_book, ab_file)
        with open("data/notebook.bin", "wb") as nb_file:
            pickle.dump(self.note_book, nb_file)
        self.exit()


if __name__ == "__main__":
    # Load/Create AddressBook
    # Load/Create NoteBook
    app = PersonalAssistant()
    app.run()
