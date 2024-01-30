"""
Personal_assistant is a personal manager for everyday tasks:
    keeping contacts - names, addresses, phone etc;
    remaindering of upcoming birthdays;
    keeping personal notes
"""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (Header,
                             Footer,
                             TabbedContent,
                             TabPane)
from pathlib import Path

from cls.NoteBook import Notebook
from cls.AddressBook import AddressBook
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

    address_book: AddressBook = AddressBook()
    note_book: Notebook = Notebook()

    def load_books(self) -> None:
        """Loads data to use in app"""
        abook_bin = Path("data/addressbook.bin")
        notebook_bin = Path("data/notebook.bin")
        if abook_bin.exists():
            with abook_bin.open('rb') as fin:
                try:
                    self.address_book = pickle.load(fin)
                except Exception as err:
                    self.notify(f"{err}", severity="error", timeout=5)
                    self.address_book = AddressBook()

        if notebook_bin.exists():
            with notebook_bin.open('rb') as fin:
                try:
                    self.note_book = pickle.load(fin)
                except Exception as err:
                    self.notify(f"notebook_trouble {err}", severity="error", timeout=5)
                    self.note_book = Notebook()

    def compose(self) -> ComposeResult:
        """Create childs for the application"""
        self.load_books()
        abook = AddressBook()
        self.notify(f"{abook == self.address_book}", timeout=10)
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
        :param tab_id: identificator for tab user clicked or entered command
        :return: None
        """
        self.get_child_by_type(TabbedContent).active = tab_id

    def action_quit(self) -> None:
        """Performes quit action"""
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
