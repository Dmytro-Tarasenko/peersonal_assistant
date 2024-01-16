"""
Notes widget
"""
from typing import List

from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import (Label,
                             Static,
                             Button,
                             TextArea,
                             DataTable,
                             ContentSwitcher,
                             Input)

from cls.NoteBook import Note, Notebook
from datetime import datetime


class NoteInput(Widget):
    '''create note tab'''
    def compose(self):
        #input_field = TextArea()
        #input_field.on_change = self.save_note
        yield TextArea(id='nt_input_text_area',
                       classes="cv_details")
        yield Horizontal(
            Label("Tags: "),
            Input(placeholder="tags go here",
                  restrict=r"[#\w\- ]+",
                  id="nt_input_tags_field"),
            classes="nt_input_inline",
            id="nt_input_inline_horiz"
        )
        yield Horizontal(
            Button('Save note',
                   id='nt_input_save_button',
                   variant="primary"),
            Button("Clear note",
                   id="nt_input_clear_note",
                   variant="error"),
            classes="nt_input_inline"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "nt_input_clear_note":
                self.query_one(TextArea).clear()
                self.query_one("Input#nt_input_tags_field").clear()
            case 'nt_input_save_button':
                text = self.query_one(TextArea).text
                tags = self.query_one("Input#nt_input_tags_field").value
                note_book: Notebook = self.app.note_book
                self.notify(f"{len(note_book.data)}")
                note_book.add_note(Note(content=text,
                                        tags=tags))
                self.notify(f"{len(note_book.data)}")


class CreateNote(Static):
    def compose(self) -> ComposeResult:
            yield NoteInput(id='note_input')


class NotesList(Widget):

    notes: List[Note] = []
    table = DataTable(classes="data_table", id="nt_dt_notes_list")

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Notes list"
        self.styles.border = ("round", "#FFD900")
        self.table = self.query_one(DataTable)
        self.table.zebra_stripes = True
        self.table.cell_padding = 2
        self.table.cursor_type = "row"
        self.table.add_column("#", width=3)
        self.table.add_column("Note created", width=18)
        self.table.add_column("Brief", width=40)
        self.table.add_column("Tags", width=40)
        self.fill_the_table()

    def fill_the_table(self, notes: List[Note] = []):
        if not notes:
            self.notes = self.app.query_one(Notes).notes
        line_num = 1
        self.notify(f"{len(self.notes)}")
        for row in self.notes:
            self.table.add_row(str(line_num),
                               row.note_id,
                               (row.content[:35]+"..."),
                               "; ".join(row.tags),
                               height=1,
                               key=row.note_id)
            line_num += 1

    def compose(self) -> ComposeResult:
        yield self.table


class NotesViewControl(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Notes Control")


class NoteDetails(Widget):
    def on_mount(self):
        self.styles.border_title_align = "left"
        self.border_title = "Notes list"
        self.styles.border = ("round", "#FFD900")

    def get_note_info(self) -> None:
        nv_main: NotesView = self.app.query_one(Notes)
        self.current_note: Note = nv_main.current_note

    def render(self) -> RenderableType:
        self.get_note_info()
        note_id = self.current_note.note_id
        created = (datetime.fromtimestamp(int(note_id))
                   .strftime("%A %d-%m-%Y %H:%M:%S"))
        content = self.current_note.content or ""
        if len(self.current_note.tags) > 0:
            tags = ", ".join(self.current_note.tags)
        else:
            tags = ""
        text = Text(tab_size=2)
        text.append("\n")
        text.append("\tCreated: ", style="bold italic #A2A2B5")
        text.append("\t" + created)
        text.append("\n")
        text.append("\tTags: ", style="bold italic #A2A2B5")
        text.append("\t" + tags)
        text.append("\n")
        text.append("\tContent: ", style="bold italic #A2A2B5")
        text.append("\t" + content)
        return text



class NotesView(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                NoteDetails(classes="nt_details",
                            id="nt_viewer_details_wdg"),
                NotesList(classes="nt_details"),
                id="nt_viewer_details"
            ),
            NotesViewControl(id="nt_viewer_ctrl")
        )


class Notes(Static):
    '''Parrent class'''
    notes: List[Note] = []
    current_note: Note = Note()
    edit_flag = False

    def compose(self):
        self.notes = list(self.app.note_book.data.values())
        if len(self.notes) > 0:
            self.current_note = self.notes[0]
        else:
            self.current_note = Note()

        with Horizontal(id="type_field"):
            yield Button("Notes List",
                         id="btn_notes_view",
                         classes="nt_btn")
            yield Button("Create Note",
                         id="btn_notes_create",
                         classes="nt_btn")

        with ContentSwitcher(initial="notes_view", id="cs_notes"):
            yield NotesView(id="notes_view")
            yield CreateNote(id="notes_create")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Switchin content by button presseed"""
        if event.button.id.startswith("btn_notes_"):
            self.query_one(ContentSwitcher).current = event.button.id.split("_", maxsplit=1)[-1]
    