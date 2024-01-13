"""
Contacts widget
"""
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (Markdown,
                             Static,
                             Button,
                             ContentSwitcher,
                             Pretty)


class ContactDetails(Widget):
    """Widget to display contact info"""
    name = reactive("name")
    bday = reactive("birthday")
    email = reactive("email")
    phones = reactive("phones")
    address = reactive("address")

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Contact details"

    def compose(self):
        str_ = """
        | Name | e-maile | Phones |
        |------|---------|--------|
        |Peter|som@gde.to|123123<br>123213213<br>888|
        
        """
        return Markdown(str_)


class ContactsView(Static):
    """Widget to display contacts list and details for selected """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                ContactDetails(classes="cv_details"),
                Markdown("Table", classes="cv_details"),
                id="cntct_viewer_details"),
            Markdown("Filter\\Find", id="cntct_viewer_ctrl")
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
