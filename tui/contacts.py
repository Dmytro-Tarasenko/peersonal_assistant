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
from textual.widgets import (Static,
                             Button,
                             ContentSwitcher,
                             DataTable,
                             Label,
                             Input)
from cls.AddressBook import Address, Record, AddressBook
from cls.validators import (BirthdayValidator,
                            EmailValidator,
                            PhoneNumberValidator,
                            NameValidator,
                            ZipCodeValidator)
from textual import on


class ContactDetails(Static):
    """Widget to display contact info"""

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Current contact details"
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

    def contact_adder(self):
        table = self.query_one(DataTable)
        table.clear()
        contacts_list: ContatsList = self.parent.query_one(ContatsList)
        contacts: Contacts = self.app.query_one(Contacts)
        contacts.records = list(self.app.address_book.data.values())
        contacts.current_record = contacts.records[0]
        contacts_list.fill_the_table()
        table.refresh()
        # line_num = 1
        # for row in self.app.address_book.data.values():
        #     table.add_row(
        #         str(line_num),
        #         row.name,
        #         row.birthday,
        #         row.address,
        #         row.email,
        #         row.phones,
        #         height=1
        #     )
        #     line_num += 1

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
                               height=1,
                               key=row.name)
            line_num += 1

    def compose(self) -> ComposeResult:
        yield self.table

    def on_data_table_row_selected(self,
                                   row_info: DataTable.RowSelected) -> None:
        contacts_wdgt: Contacts = self.app.query_one("Contacts")
        address_book: AddressBook = self.app.address_book
        contacts_wdgt.current_record = address_book.data[row_info.row_key.value]
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
            with Horizontal():
                yield Button("Lookup", variant="primary", id="cv_control_lookup")
                yield Button("Clear Search", variant="warning", id="cv_control_clear")
            with Horizontal():
                yield Button("Edit record", variant="warning", id="cv_control_edit")
                yield Button("Delete record", variant="error", id="cv_control_delete")

    def cv_control_lookup(self) -> None:
        inputs: List[Input] = self.query("Input.cv_input")
        search_conditions = []
        address_book: AddressBook = self.app.address_book
        for input_ in inputs:
            field = input_.id.rsplit("_")[-1]
            if input_.value:
                search_conditions.append(f"%{field.upper()}%{input_.value}")
        if len(search_conditions) == 0:
            self.notify("No search conditions are specified!",
                        severity="warning",
                        timeout=10)
        records: List[Record] = address_book.find_record(search_conditions)
        if len(records) == 0:
            self.notify("Search returned no results!",
                        severity="warning",
                        timeout=8)
        contacts_list: ContatsList = self.parent.query_one(ContatsList)
        contacts_list.records = records
        contacts_list.table.clear()
        contacts_list.fill_the_table(records)
        contacts_list.refresh()

    def cv_control_clear(self) -> None:
        inputs: List[Input] = self.query("Input.cv_input")
        for input_ in inputs:
            input_.clear()
        contacts_list: ContatsList = self.parent.query_one(ContatsList)
        contacts_list.table.clear()
        contacts_list.fill_the_table()
        contacts_list.refresh()

    def cv_control_delete(self) -> None:
        record: Record = self.app.query_one(Contacts).current_record
        self.app.address_book.delete_record(record.name)
        table = self.parent.query_one(DataTable)
        table.clear()
        contacts_list: ContatsList = self.parent.query_one(ContatsList)
        contacts: Contacts = self.app.query_one(Contacts)
        contacts.records = list(self.app.address_book.data.values())
        if contacts.records:
            contacts.current_record = contacts.records[0]
        else:
            contacts.current_record = Record()
        contacts_list.fill_the_table()
        table.refresh()

    def cv_control_edit(self) -> None:
        self.app.query_one(Contacts).edit_flag = True
        record: Record = self.app.query_one(Contacts).current_record
        address: Address = record.address
        editor: ContactsEdit = self.app.query_one(ContactsAdd)
        inputs: List[Input] = editor.query(Input)
        for field in inputs:
            match field.id:
                case "name_input":
                    if name := record.name:
                        field.value = name
                case "phone_input":
                    if phones := record.phones:
                        field.value = " ".join(phones)
                case "birthday_input":
                    if birthday:= record.birthday:
                        field.value = birthday
                case "email_input":
                    if email := record.email:
                        field.value = email
                case "zipcode_input":
                    if address:
                        if zip_code := address.zip_code:
                            field.value = str(zip_code)
                case "country_input":
                    if address:
                        if country := address.country:
                            field.value = country
                case "city_input":
                    if address:
                        if city := address.city:
                            field.value = city
                case "street_input":
                    if address:
                        if street := address.street:
                            field.value = street
                case "house_input":
                    if address:
                        if house := address.house:
                            field.value = str(house)
                case "apartment_input":
                    if address:
                        if apartment := address.apartment:
                            field.value = str(apartment)
        switcher: ContentSwitcher = (self.app.query_one(Contacts)
                                     .query_one(ContentSwitcher))
        switcher.current = "contacts_adder"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Process Lookup button pressed"""
        match event.button.id:
            case "cv_control_lookup":
                self.cv_control_lookup()
            case "cv_control_clear":
                self.cv_control_clear()
            case "cv_control_edit":
                self.cv_control_edit()
            case "cv_control_delete":
                self.cv_control_delete()


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
    def __init__(self, widget_value_name='', widget_value_phone=None,
                 widget_value_birthday=None, widget_value_email=None,
                 widget_value_zipcode=None, widget_value_country=None, widget_value_city=None,
                 widget_value_street=None, widget_value_house=None, widget_value_apartment=None,
                 address_book=AddressBook, **kwargs):
        super().__init__(**kwargs)
        self.widget_value_name = widget_value_name
        self.widget_value_phone = widget_value_phone
        self.widget_value_birthday = widget_value_birthday
        self.widget_value_email = widget_value_email
        self.widget_value_zipcode = widget_value_zipcode
        self.widget_value_country = widget_value_country
        self.widget_value_city = widget_value_city
        self.widget_value_street = widget_value_street
        self.widget_value_house = widget_value_house
        self.widget_value_apartment = widget_value_apartment
        self.address_book = address_book

    def compose(self) -> ComposeResult:
        with Grid(id="cv_adder_editor"):
            yield Vertical(
                Label('Enter user`s name (only alphabetic characters|first letter must be capital)'),
                Input(
                    placeholder="Enter user name...",
                    validators=[NameValidator()],
                    id="name_input")
            )
            yield Vertical(
                Label("Enter user`s phone number (10 digits):"),
                Input(placeholder="Enter phone number...",
                      validators=[PhoneNumberValidator()],
                      id="phone_input")
            )
            yield Vertical(
                Label("Enter user`s birthday (in format DD-MM-YYYY)"),
                Input(placeholder="Enter user birthday...",
                      validators=[BirthdayValidator()],
                      id="birthday_input")
            )
            yield Vertical(
                Label("Enter user`s email address (Exa.mple123@email.com)"),
                Input(placeholder="Enter user email...",
                      validators=[EmailValidator()],
                      id="email_input",
                      restrict=None)
            )
            yield Vertical(
                Label("Enter user`s zip code"),
                Input(placeholder="Enter zip code",
                      validators=[ZipCodeValidator()],
                      id="zipcode_input")
            )
            yield Vertical(
                Label("Enter user`s country"),
                Input(placeholder="Enter country...",
                      id="country_input")
            )
            yield Vertical(
                Label("Enters user`s city"),
                Input(placeholder="Enter city...",
                      id="city_input")
            )
            yield Vertical(
                Label("Enter user`s street"),
                Input(placeholder="Enter street...",
                      id="street_input")
            )
            yield Vertical(
                Label("Enter user`s № house"),
                Input(placeholder="Enter № house...",
                      id="house_input")
            )
            yield Vertical(
                Label("Enter user`s № apartment"),
                Input(placeholder="Enter № apartment...",
                      id="apartment_input")
            )

        yield Button(label="Submit info", id="add_info")

    @on(Button.Pressed)
    def accept_info(self):
        input_widgets = self.query(Input)

        name_widget = None
        phone_widget = None
        birthday_widget = None
        email_widget = None
        zipcode_widget = None
        country_widget = None
        city_widget = None
        street_widget = None
        house_widget = None
        apartment_widget = None

        validation_errors = []

        for widget in input_widgets:
            validation_result = widget.validate(widget.value)

            if validation_result is not None and not validation_result.is_valid:
                error_message = validation_result.failure_descriptions[0]
                self.notify(message=error_message, title='Error', severity='error', timeout=7)  # Вивід повідомлення
            else:
                if widget.id == "name_input":
                    name_widget = widget.value
                elif widget.id == "phone_input":
                    phone_widget = widget.value
                elif widget.id == "birthday_input":
                    birthday_widget = widget.value
                elif widget.id == "email_input":
                    email_widget = widget.value
                elif widget.id == 'zipcode_input':
                    zipcode_widget = widget.value
                elif widget.id == "country_input":
                    country_widget = widget.value
                elif widget.id == "city_input":
                    city_widget = widget.value
                elif widget.id == "street_input":
                    street_widget = widget.value
                elif widget.id == "house_input":
                    house_widget = widget.value
                elif widget.id == "apartment_input":
                    apartment_widget = widget.value

        if not validation_errors:
            if all([phone_widget, email_widget, birthday_widget, zipcode_widget,
                    country_widget, city_widget, street_widget, house_widget, apartment_widget]) or name_widget:
                self.notify(message="User`s information added to address book", title='Success',
                            severity='information', timeout=7)
                record = Record(
                    name=name_widget,
                    phones=[phone_widget] if phone_widget else None,
                    birthday=birthday_widget if birthday_widget else None,
                    email=email_widget if email_widget else None,
                    address=Address(
                        country=country_widget if country_widget else "",
                        zip_code=zipcode_widget if zipcode_widget else "",
                        city=city_widget if city_widget else "",
                        street=street_widget if street_widget else "",
                        house=house_widget if house_widget else "",
                        apartment=apartment_widget if apartment_widget else ""
                    )
                )
                if self.app.query_one(Contacts).edit_flag:
                    self.app.address_book.delete_record(record.name)
                    self.app.query_one(Contacts).edit_flag = False
                self.app.address_book.add_record(record)
                contacts_list = self.app.query_one(ContatsList).refresh()
                contacts_list.contact_adder()
                for widget in input_widgets:
                    widget.value = ''
                switcher: ContentSwitcher = (self.app.query_one(Contacts)
                                             .query_one(ContentSwitcher))
                switcher.current = "contacts_viewer"


class Contacts(Static):
    """Container widger for Contacts tab"""
    current_record: Record = Record()
    records: List[Record] = []
    edit_flag = False

    def compose(self) -> ComposeResult:
        """Composing main elements"""
        self.records = list(self.app.address_book.data.values())
        if len(self.records) > 0:
            self.current_record = self.records[0]
        else:
            self.current_record = Record()

        with Horizontal(id="contacts_workspaces"):
            yield Button("View contacts", id="btn_contacts_viewer")
            yield Button("Add\\Edit contacts", id="btn_contacts_adder")

        with ContentSwitcher(initial="contacts_viewer", id="cs_contacts"):
            yield ContactsView(id="contacts_viewer")
            yield ContactsAdd(id="contacts_adder")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Switchin content by button presseed"""
        if event.button.id.startswith("btn_contacts_"):
            self.query_one(ContentSwitcher).current = event.button.id.split("_", maxsplit=1)[-1]
