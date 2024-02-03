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
                             Input, Rule)

from cls.NoteBook import Note, Notebook
from datetime import datetime

from cls.PimpConfig import PimpConfig


class NoteInput(Widget):
    """create note tab"""
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
                if self.app.query_one(Notes).edit_flag:
                    note = self.app.query_one(Notes).current_note
                    self.app.note_book.delete_record(note)
                    self.app.query_one(Notes).edit_flag = False
                text = self.query_one(TextArea).text
                tags = self.query_one("Input#nt_input_tags_field").value.split()
                note_book: Notebook = self.app.note_book
                note_book.add_record(Note(content=text,
                                        tags=tags))
                notes_list = self.app.query_one(NotesList).refresh()
                notes_list.note_adder()
                self.notify("Note`s info added", severity="information", timeout=7)
                self.query_one(TextArea).clear()
                self.query_one("Input#nt_input_tags_field").clear()
                switcher: ContentSwitcher = (self.app.query_one(Notes)
                                             .query_one(ContentSwitcher))
                switcher.current = "notes_view"


class CreateNote(Static):
    def compose(self) -> ComposeResult:
            yield NoteInput(id='note_input')


class NotesList(Widget):

    notes: List[Note] = []
    table = DataTable(classes="data_table", id="nt_dt_notes_list")

    def note_adder(self):
        table = self.query_one(DataTable)
        table.clear()
        notes_list: NotesList = self.parent.query_one(NotesList)
        notes: Notes = self.app.query_one(Notes)
        notes.notes = list(self.app.note_book.data.values())
        notes.current_note = notes.notes[0]
        notes_list.fill_the_table()
        table.refresh()

    def on_mount(self) -> None:
        self.styles.border_title_align = "left"
        self.border_title = "Notes list"
        self.styles.border = ("round", "#FFD900")
        self.table = self.query_one(DataTable)
        self.table.zebra_stripes = True
        self.table.cell_padding = 2
        self.table.cursor_type = "row"
        self.table.add_column("#", width=3)
        self.table.add_column("Note created", width=14)
        self.table.add_column("Brief", width=38)
        self.table.add_column("Tags", width=40)
        self.fill_the_table()

    def fill_the_table(self, notes: List[Note] = []):
        if not notes:
            self.notes = self.app.query_one(Notes).notes
        line_num = 1
        for row in self.notes:
            created = (datetime.fromtimestamp(row.note_id)
                       .strftime("%a %d-%m-%Y %H:%M:%S"))
            self.table.add_row(str(line_num),
                               created,
                               (row.content[:35]+"..."),
                               "; ".join(row.tags),
                               height=1,
                               key=row.note_id)
            line_num += 1

    def compose(self) -> ComposeResult:
        yield self.table

    def on_data_table_row_selected(self,
                                   row_info: DataTable.RowSelected) -> None:
        notes_wdgt: Notes = self.app.query_one("Notes")
        note_book: Notebook = self.app.note_book
        notes_wdgt.current_note = note_book.data[row_info.row_key.value]
        details_wdgt: NoteDetails = self.parent.query_one("#nt_viewer_details_wdgt")
        details_wdgt.get_note_info()
        details_wdgt.update()


class NotesViewControl(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="nt_controls"):
            yield Label("Words to search:",
                        classes="nt_input")
            yield Input(placeholder="full word search",
                        classes="nt_input",
                        restrict=r"[a-zA-Z_ ]*",
                        id="nt_control_word")

            yield Label("Tags to search:",
                        classes="nt_input")
            yield Input(placeholder="search tags go here",
                        classes="nt_input",
                        restrict=r"[a-zA-Z_ ]*",
                        id="nt_control_tags")

            yield Rule()
            with Horizontal():
                yield Button("Lookup",
                             variant="primary",
                             id="nt_btn_control_lookup")
                yield Button("Clear Search",
                             variant="warning",
                             id="nt_btn_control_clear")

            yield Rule()
            with Horizontal():
                yield Button("Edit note",
                             variant="warning",
                             id="nt_btn_control_edit")
                yield Button("Delete note",
                             variant="error",
                             id="nt_btn_control_delete")

    def nt_control_lookup(self) -> None:
        inputs: List[Input] = self.query("Input.nt_input")
        full_words = []
        tags = []
        note_book: Notebook = self.app.note_book
        for input_ in inputs:
            match input_.id:
                case "nt_control_word":
                    full_words.extend(input_.value.split(" "))
                case "nt_control_tags":
                    tags.extend(input_.value.split(" "))
        notes: List[Note] = []
        notes_by_word: List[Note] = []
        notes_by_tag: List[Note] = []
        if len(full_words) > 0:
            notes.extend(note_book.find_notes_by_keyword(full_words))
        if len(tags) > 0:
            notes.extend(note_book.find_notes_by_tags(tags))
        notes.extend(notes_by_tag)
        for note in notes_by_word:
            if note not in notes:
                notes.append(note)
        if len(notes) == 0:
            self.notify("Search returned no results!",
                        severity="warning",
                        timeout=8)
            return
        notes_list: NotesList = self.parent.query_one(NotesList)
        notes_list.notes = notes
        notes_list.table.clear()
        notes_list.fill_the_table(notes)
        notes_list.refresh()

    def nt_control_clear(self) -> None:
        inputs: List[Input] = self.query("Input.nt_input")
        for input_ in inputs:
            input_.clear()
        notes_list: NotesList = self.parent.query_one(NotesList)
        notes_list.table.clear()
        notes_list.fill_the_table()
        notes_list.refresh()

    def nt_control_delete(self) -> None:
        note: Note = self.app.query_one(Notes).current_note
        self.app.note_book.delete_record(note)
        table = self.parent.query_one(DataTable)
        table.clear()
        note_list: NotesList = self.parent.query_one(NotesList)
        notes: Notes = self.app.query_one(Notes)
        notes.notes = list(self.app.note_book.data.values())
        if notes.notes:
            notes.current_note = notes.notes[0]
        else:
            notes.current_note = Note()
        self.notify("Note is deleted.", severity="warning", timeout=7)
        note_list.fill_the_table()
        table.refresh()
        note_list.refresh()

    def nt_control_edit(self) -> None:
        self.app.query_one(Notes).edit_flag = True
        note: Note = self.app.query_one(Notes).current_note
        editor: NoteInput = self.app.query_one(NoteInput)
        content: TextArea = editor.query_one(TextArea)
        tags: Input = editor.query_one("Input#nt_input_tags_field")
        content.text = note.content
        tags.value = " ".join(note.tags)
        switcher: ContentSwitcher = (self.app.query_one(Notes)
                                     .query_one(ContentSwitcher))
        switcher.current = "notes_create"


    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "nt_btn_control_lookup":
                self.nt_control_lookup()
            case "nt_btn_control_clear":
                self.nt_control_clear()
            case "nt_btn_control_edit":
                self.nt_control_edit()
            case "nt_btn_control_delete":
                self.nt_control_delete()


class NoteDetails(Static):
    def on_mount(self):
        self.styles.border_title_align = "left"
        self.border_title = "Note info"
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
                            id="nt_viewer_details_wdgt"),
                NotesList(classes="nt_details"),
                id="nt_viewer_details"
            ),
            NotesViewControl(id="nt_viewer_ctrl")
        )


class Notes(Static):
    """Parrent class"""
    app_config = PimpConfig()
    notes: List[Note] = []
    current_note: Note = Note()
    edit_flag = False

    def compose(self):
        self.notes = list(self.app_config.note_book.data.values())
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
    