"""
Contacts widget
"""
from typing import List

from rich.console import RenderableType
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Grid
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (Markdown,
                             Static,
                             Button,
                             ContentSwitcher, DataTable, Label, Input)
from cls.AddressBook import Address, AddressBook, Record


class ContactDetails(Static):
    """Widget to display contact info"""

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Contact details"
        self.styles.border = ("round", "#FFD900")

    def get_record_info(self) -> None:
        """Sets attributes according ro Record fields"""
        cv_main: ContactsView = self.app.query_one("Contacts")
        self.current_record: Record = cv_main.current_record

    def render(self) -> RenderableType:
        self.get_record_info()
        name = self.current_record.name
        bday = self.current_record.birthday
        address = self.current_record.address
        email_ = self.current_record.email
        phones = self.current_record.phones

        return f"sdfsdf{self.current_record}"


class ContatsList(Widget):
    """Widget to display list of contacts"""
    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Contacts list"
        self.styles.border = ("round", "#FFD900")
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cell_padding = 2
        table.cursor_type = "row"
        table.add_column("#", width=3)
        table.add_column("Name", width=10)
        table.add_column("Birhday", width=10)
        table.add_column("Address", width=20)
        table.add_column("e-mail", width=18)
        table.add_column("Phones", width=20)
        line_num = 1
        contacts_wdgt: Contacts = self.app.query_one("Contacts")
        for row in contacts_wdgt.records:
            table.add_row(str(line_num),
                          row.name,
                          row.birthday,
                          row.address,
                          row.email,
                          row.phones,
                          height=1)
            line_num += 1

    def compose(self) -> ComposeResult:
        yield DataTable(classes="data_table", id="contacts_list")

    def on_data_table_row_selected(self, row_info: Message) -> None:
        contacts_wdgt: Contacts = self.app.query_one("Contacts")
        contacts_wdgt.current_record = contacts_wdgt.records[row_info.cursor_row]
        details_wdgt: ContactDetails = self.parent.query_one("#contact_details_wdgt")
        details_wdgt.get_record_info()
        details_wdgt.update()


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


class ContactsView(Static):
    """Widget to display contacts list and details for selected """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                ContactDetails(id="contact_details_wdgt",
                               classes="cv_details"),
                ContatsList(classes="cv_details"),
                id="cntct_viewer_details"),
            ContactsViewControl(id="cntct_viewer_ctrl")
        )


class ContactsAdd(Static):
    """Widget to add contact """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Record info", classes="cntct_add_fields"),
            Label("Add fileds", classes="cntct_add_fields")
        )


class ContactsEdit(Static):
    """Widget to edit/delete contacts """
    def compose(self) -> ComposeResult:
        yield Markdown("**Contact** editor")


class Contacts(Static):
    """Container widger for Contacts tab"""
    current_record: Record = Record()
    records: List[Record] = []
    super_address: Address = Address()

    def compose(self) -> ComposeResult:
        self.records = list(self.app.address_book.data.values())
        self.current_record = self.records[0]
        self.super_address = self.current_record.address
        self.super_address.zip_code = 54321
        self.current_record.address = self.super_address
        self.notify(f"{self.current_record.address}", severity="information", timeout=15)
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
