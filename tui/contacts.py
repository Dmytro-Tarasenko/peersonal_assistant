"""
Contacts widget
"""
from rich.console import RenderableType
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Grid
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (Markdown,
                             Static,
                             Button,
                             ContentSwitcher, DataTable, Label, Input)
from cls.AddressBook import Address, AddressBook, Email, Record, Phone
from datetime import date


class ContactDetails(Widget):
    """Widget to display contact info"""
    name = reactive("name")
    bday = reactive("birthday")
    email = reactive("email")
    phones = reactive("phones")
    address = reactive("address")
    current_record = reactive(None)

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Contact details"

    def get_record_info(self) -> None:
        """Sets attributes according ro Record fields"""
        cv_main: ContactsView = self.app.query_one("Contacts")
        self.current_record: Record = cv_main.current_record
        self.notify(f"{self.current_record.name}", timeout=5, severity="information")
        self.name = str(self.current_record.name)
        self.bday = str(self.current_record.birthday)
        self.email = str(self.current_record.email)
        self.phones = str(self.current_record.phones)
        self.address = str(self.current_record.address)

    def compose(self) -> ComposeResult:
        self.get_record_info()
        yield Grid(
            Horizontal(
                Label("Name: "),
                Label(str(self.name)),
                classes="grid_box"
            ),
            Horizontal(
                Label("Phones: "),
                Label(self.phones),
                classes="grid_box"
            ),
            Horizontal(
                Label("Birthday: "),
                Label(self.bday),
                classes="grid_box"
            ),
            Horizontal(
                Label("Email: "),
                Label(self.email),
                classes="grid_box"
            ),
            Horizontal(
                Label("Address: "),
                Label(self.address),
                classes="grid_box"
            ),
            id="cd_grid"
        )


class ContatsList(Widget):
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cell_padding = 2
        table.cursor_type = "row"
        table.add_columns("#", "Name", "Age")
        table.add_row("1", "Engelgardt asdasd", "43")
        table.add_row("2", "Shevchenko", "12")
        table.add_row("3", "Engelgardt", "123")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Contacts list:"),
            DataTable(classes="data_table", id="contacts_list")
        )


class ButtonPressed:
    pass


class ContactsViewControl(Widget):
    """Widget contains control element for contact filtering\\searchin"""
    def compose(self) -> ComposeResult:
        with Vertical(id="cv_controls"):
            yield Label("Enter at least 3 characters",
                        classes="cv_input")
            yield Input(placeholder="Name\\part to lookup",
                        classes="cv_input")
            yield Label("Enter at least 3 digits",
                        classes="cv_input")
            yield Input(placeholder="Phone\\part  to lookup",
                        classes="cv_input")
            yield Label("Enter at least 3 characters",
                        classes="cv_input")
            yield Input(placeholder="E-mail\\part to lookup",
                        classes="cv_input")
            yield Label("Enter at least 3 symbols",
                        classes="cv_input")
            yield Input(placeholder="Address\\part to lookup",
                        classes="cv_input")
            yield Button("Lookup", variant="primary")

    def on_button_pressed(self, event: ButtonPressed):
        """Placeholder gor future"""
        pass


class ContactsView(Static):
    """Widget to display contacts list and details for selected """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                ContactDetails(classes="cv_details"),
                ContatsList(classes="cv_details"),
                id="cntct_viewer_details"),
            ContactsViewControl(id="cntct_viewer_ctrl")
        )


class ContactsAdd(Static):
    """Widget to add contact """
    def compose(self) -> ComposeResult:
        yield Markdown("**Contact adder**")


class ContactsEdit(Static):
    """Widget to edit/delete contacts """
    def compose(self) -> ComposeResult:
        yield Markdown("**Contact** editor")


class Contacts(Static):
    """Container widger for Contacts tab"""
    current_record: Record = Record(name="Taras Shevchenko",
                                    birthday="09-03-1814",
                                    email=None,
                                    address=Address(country="Ukraine",
                                                    zip_code=12345,
                                                    city="s. Moryntsi",
                                                    street="Vyshneva",
                                                    house="12",
                                                    apartment="1"),
                                    phones=[Phone(123),
                                            Phone(23423),
                                            Phone(4323)]
                                    )
    addressbook = AddressBook()
    addressbook.add_record(current_record)

    def compose(self) -> ComposeResult:
        """Composing main elements"""
        with Horizontal(id="contacts_workspaces"):
            yield Button("View contacts", id="contacts_viewer")
            yield Button("Add contacts", id="contacts_adder")
            yield Button("Edit\\Delete contacts", id="contacts_editor")

        with ContentSwitcher(initial="contacts_viewer", id="cs_contacts"):
            yield ContactsView(id="contacts_viewer")
            yield ContactsAdd(id="contacts_adder")
            yield ContactsEdit(id="contacts_editor")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Switchin content by button presseed"""
        self.query_one(ContentSwitcher).current = event.button.id

    def on_mount(self) -> None:
        initial: Widget = self.query_one("Static#contacts_viewer")
        initial.refresh()
