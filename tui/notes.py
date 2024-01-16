"""
Notes widget
"""
from typing import List

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Grid
from textual import on
from textual.events import Mount
from textual.widget import Widget
from textual.widgets import Markdown, Label, Static, Button, TextArea, DataTable, ContentSwitcher
from cls.NoteBook import Note, Notebook

class NoteDetails(Static):
    """Widget displays saved notes"""

    def on_mount(self) -> None:
        self.border_title = "My Note"
        self.styles.border = ("round", "#FFD900")

    def get_notes_text(self) -> None:
        pass

    def render(self):
        pass


class NoteList2(Widget):

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "All Notes"
        self.styles.border = ("round", "#FFD900")
        table = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cell_padding = 2
        table.cursor_type = "row"
        table.add_column("#", width=3)
        table.add_column("Note", width=10)
        table.add_column("Create Date", width=10)
        line_num = 1
        contacts_wdgt: "Contacts" = self.app.query_one("Contacts")
        for row in contacts_wdgt.records:
            table.add_row(str(line_num),
                          row.name,
                          row.birthday,
                          row.address,
                          row.email,
                          row.phones,
                          height=1)
            line_num += 1


class NotesView(Static):
    """Widget displays notes list and details for selected """
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                NoteDetails(id="contact_details_wdgt",
                               classes="cv_details"),
                NoteDetails(classes="cv_details"),
                id="cntct_viewer_details"),
            #ContactsViewControl(id="cntct_viewer_ctrl")
        )



class NoteInput(Static):
    '''create note tab'''
    def compose(self):
        #input_field = TextArea()
        #input_field.on_change = self.save_note
        yield TextArea(id='text_area', classes="cv_details")
        yield Horizontal(
            Label("Tags: ")
        )
        yield Button('Save note', id='save_button')

    @on(Button.Pressed)
    def save_note(self):
        input_field = self.query_one(TextArea)
        my_note = input_field.text

        if my_note:
            self.notebook.add_note(my_note)
            self.notify(f'{len(self.notebook.notes)}', severity="information", timeout=10)
            input_field.text = ''
            #self.refresh_notes_view()


class CreateNote(Static):
    def compose(self) -> ComposeResult:
            yield NoteInput(id='note_input')



class NotesList(Static):

    def compose(self) -> ComposeResult:
        yield Label('test2')
        

class Notes(Static):
    '''Parrent class'''
    current_note: Note = Note()
    notes: List[Note] = []

    def __init__(self):
        super().__init__()
        self.notebook: Notebook = self.app.note_book

    def compose(self):
        with Vertical():
            with Horizontal(id="type_field"):
                yield Button("Create Note",
                             id="btn_notes_create",
                             classes="nt_btn")
                yield Button("Notes List",
                             id="btn_notes_list",
                             classes="nt_btn")

            with ContentSwitcher(initial="notes_create", id="cs_notes"):
                yield CreateNote(id="notes_create",
                                 classes="nt_details")
                yield NotesList(id="notes_list",
                                classes="nt_details")
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Switchin content by button presseed"""
        if event.button.id.startswith("btn_notes_"):
            self.query_one(ContentSwitcher).current = event.button.id.split("_", maxsplit=1)[-1]
    