"""
Contacts widget
"""
from typing import List

from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Grid
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (Markdown,
                             Static,
                             Button,
                             ContentSwitcher, DataTable, Label, Input)
from cls.AddressBook import Address, Record, AddressBook


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
        text = Text(tab_size=1)
        text.append("\n")
        text.append("\tName: ", style="bold italic #A2A2B5")
        text.append("\t"+name)
        text.append("\tBirthday: ", style="bold italic #A2A2B5")
        text.append("\t"+bday)
        text.append("\n\n")
        text.append("\te-mail: ", style="bold italic #A2A2B5")
        text.append("\t"+email_)
        text.append("\n\n")
        text.append("\tAddress: ", style="bold italic #A2A2B5")
        text.append("\t" + str(address))
        text.append("\n\n")
        text.append("\tPhones: ", style="bold italic #A2A2B5")
        text.append("\t" + ",".join(phones))
        return text


class ContatsList(Widget):
    """Widget to display list of contacts"""
    records: List[Record] = []
    table = DataTable(classes="data_table", id="contacts_list")

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Contacts list"
        self.styles.border = ("round", "#FFD900")
        self.table = self.query_one(DataTable)
        self.table.zebra_stripes = True
        self.table.cell_padding = 2
        self.table.cursor_type = "row"
        self.table.add_column("#", width=3)
        self.table.add_column("Name", width=10)
        self.table.add_column("Birhday", width=10)
        self.table.add_column("Address", width=20)
        self.table.add_column("e-mail", width=18)
        self.table.add_column("Phones", width=20)
        self.fill_the_table()

    def fill_the_table(self, records: List[Record] = []):
        if not records:
            self.records = self.app.query_one("Contacts").records
        line_num = 1
        for row in self.records:
            self.table.add_row(str(line_num),
                          row.name,
                          row.birthday,
                          row.address,
                          row.email,
                          ",".join(row.phones),
                          height=1)
            line_num += 1

    def compose(self) -> ComposeResult:
        yield self.table

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
                        classes="cv_input",
                        restrict=r"\w+",
                        id="cv_control_name")
            yield Label("Enter from 3 to 10 digits",
                        classes="cv_input")
            yield Input(placeholder="Phone\\part  to lookup",
                        classes="cv_input",
                        type="integer",
                        restrict=r"\d{,10}",
                        id="cv_control_phones")
            yield Label("Enter at least 3 characters",
                        classes="cv_input")
            yield Input(placeholder="E-mail\\part to lookup",
                        classes="cv_input",
                        restrict=r"[\w.@]+",
                        id="cv_control_email")
            yield Label("Enter at least 3 symbols",
                        classes="cv_input")
            yield Input(placeholder="Address\\part to lookup",
                        classes="cv_input",
                        restrict=r"[\w.,-]+",
                        id="cv_control_address")
            yield Button("Lookup", variant="primary", id="cv_control_lookup")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Process Lookup button pressed"""
        inputs: List[Input] = self.query("Input.cv_input")
        search_conditions = []
        address_book: AddressBook = self.app.address_book
        for input in inputs:
            field = input.id.rsplit("_")[-1]
            if input.value:
                search_conditions.append(f"%{field.upper()}%{input.value}")
        if len(search_conditions) == 0:
            self.notify("No search conditions are specified!",
                        severity="warning",
                        timeout=10)
        records: List[Record] = address_book.find_record(search_conditions)
        contacts_list: ContatsList = self.parent.query_one(ContatsList)
        contacts_list.records = records
        self.notify(f"{records}", severity="information", timeout=10)
        contacts_list.table.clear()
        contacts_list.fill_the_table(records)
        contacts_list.refresh()


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

    def compose(self) -> ComposeResult:
        """Composing main elements"""
        self.records = list(self.app.address_book.data.values())
        self.current_record = self.records[0]

        with Horizontal(id="contacts_workspaces"):
            yield Button("View contacts", id="btn_contacts_viewer")
            yield Button("Add contacts", id="btn_contacts_adder")
            yield Button("Edit\\Delete contacts", id="btn_contacts_editor")

        with ContentSwitcher(initial="contacts_viewer", id="cs_contacts"):
            yield ContactsView(id="contacts_viewer")
            yield ContactsAdd(id="contacts_adder")
            yield ContactsEdit(id="contacts_editor")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Switchin content by button presseed"""
        if event.button.id.startswith("btn_contacts_"):
            self.query_one(ContentSwitcher).current = event.button.id.split("_", maxsplit=1)[-1]

    # def on_mount(self) -> None:
    #     initial: Widget = self.query_one("ContactsView")
    #     initial.refresh()
