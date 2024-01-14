"""
File Sorter widget
"""
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, DirectoryTree, Button
from pathlib import Path

from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode


class DirTreeSelected(Static):
    """Static widget for displaying selected directory"""
    selected = reactive(str(Path.cwd()))

    def on_mount(self):
        dir_tree: DirectoryTree = self.parent.query_one("#file_sorter_tree")
        self.selected = dir_tree.path

    def render(self) -> str:
        return f"Selected: {self.selected}"


class Sorter(Static):
    """File Sorter main widget"""
    cur_dir = Path.cwd()
    dir_tree = DirectoryTree(cur_dir, id="file_sorter_tree")
    drives = [chr(x) + ":" for x in range(65, 91)
              if Path.exists(Path(chr(x) + ":"))]
    buttons = []

    for drive in drives:
        label = drive.upper()
        id_ = drive.replace(":", "_drive")
        buttons.append(Button(label,
                              variant="default",
                              classes="tree_button",
                              id=id_))
    if len(buttons) == 0:
        buttons = [Button("/",
                          variant="primary",
                          classes="tree_button",
                          id="root_drive")]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                *self.buttons,
                Button("^Up^",
                       variant="primary",
                       classes="tree_button",
                       id="up_tree"),
                id="sorter_tree_buttons"
            ),
            self.dir_tree,
            DirTreeSelected(id="dir_selected"),
            Button("Sort selected", variant="default", id="sort_folder")
        )

    def on_directory_tree_directory_selected(self,
                                             node: TreeNode[DirEntry])\
            -> None:
        """
        Sets the selected in DirTreeSelected
        Parameters:
            node (TreeNode[DirEntry]): contains selected folder

        """
        selected: DirTreeSelected = self.query_one("#dir_selected")
        dir_tree: DirectoryTree = self.query_one("#file_sorter_tree")
        dir_tree.path = selected.selected = node.path
        selected.refresh()
        dir_tree.refresh()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event Handler for Buttons
        Parameters:
            event (Button.Pressed): contains info for pressed Button
        """
        # up_button: Button = self.query_one("#up_tree")
        drive_tree = self.query_one(DirectoryTree)
        selected: DirTreeSelected = self.query_one("#dir_selected")

        if event.button.id.endswith("_drive"):
            new_path = event.button.id.split("_")[0]
            self.cur_dir = Path("/") if new_path == "root" else Path(new_path+":")
        elif event.button.id == "up_tree":
            self.cur_dir = self.cur_dir.parent
        else:
            return
        drive_tree.path = selected.selected = self.cur_dir
        drive_tree.refresh()
        selected.refresh()
