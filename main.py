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

from cls.AddressBook import AddressBook
from tui import dashboard, contacts, notes, settings, sorter
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
        ("s", "show_tab('settings')", "Settings"),
        Binding("ctrl+c", "quit", "Save all and quit",
                show=True, priority=True)
    ]

    CSS_PATH = ["tcss/main.tcss",
                "tcss/dashboard.tcss",
                "tcss/sorter.tcss",
                "tcss/contacts.tcss"]

    address_book = AddressBook()
    # note_book = NoteBook()

    def load_books(self) -> None:
        """Loads data to use in app"""
        abook_bin = Path("data/addressbook.bin")
        # nbook_bin = Path("data/notebook.bin")
        if abook_bin.exists():
            with abook_bin.open('rb') as fin:
                try:
                    self.address_book = pickle.load(fin, fix_imports=False)
                except Exception as err:
                    self.notify(f"{err}", severity="error", timeout=5)
                    self.address_book = AddressBook()

        # if nbook_bin.exists():
        #     with nbook_bin.open('rb') as fin:
        #         try:
        #             self.note_book = pickle.load(fin, fix_imports=False)
        #         except Exception as err:
        #             self.notify(f"{err}", severity="error", timeout=5)
        #             self.note_book = NoteBook()

    def on_mount(self):
        self.load_books()

    def compose(self) -> ComposeResult:
        """Create childs for the application"""
        yield Header()
        yield Footer()

        with TabbedContent():
            with TabPane("Dashboard", id="dashbrd"):
                yield dashboard.DashBoard()
            with TabPane("Contacts", id="contacts"):
                yield contacts.Contacts()
            with TabPane("Notes", id="notes"):
                yield notes.paNotes
            with TabPane("Settings", id="settings"):
                yield settings.paSettings
            with TabPane("File Sorter", id="sort"):
                yield sorter.Sorter()

    def action_show_tab(self, tab_id: str) -> None:
        """
        Switching tabs by id
        :param tab_id: identificator for tab user clicked or entered command
        :return: None
        """
        self.get_child_by_type(TabbedContent).active = tab_id

    def action_quit(self) -> None:
        """Performes quit action"""
        with open("addressbook.dat", "a") as ab_file:
            ab_file.write("AddressBook is saved\n")
        with open("notebook.dat", "a") as nb_file:
            nb_file.write("AddressBook is saved\n")
        self.exit()


if __name__ == "__main__":
    # Load/Create AddressBook
    # Load/Create NoteBook
    app = PersonalAssistant()
    app.run()
