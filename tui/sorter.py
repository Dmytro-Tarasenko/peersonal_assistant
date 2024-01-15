from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widgets import Static, DirectoryTree, Button
from modules.sorted_folder import sorted_folder
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode
from pathlib import Path
from os.path import exists
import os
import sys


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)


class DirTreeSelected(Static):
    """
    Widget to display and track the selected directory in the DirectoryTree.
    """
    selected = reactive(str(Path.cwd()))

    def on_mount(self):
        """Event handler when the widget is mounted."""
        dir_tree: DirectoryTree = self.parent.query_one("#file_sorter_tree")
        self.selected = dir_tree.path

    def render(self) -> str:
        """Render the widget."""
        return f"Selected: {self.selected}"


class Sorter(Static):
    """
    Widget for file sorting with a DirectoryTree and sorting buttons.
    """
    cur_dir = Path.cwd()
    dir_tree = DirectoryTree(cur_dir, id="file_sorter_tree")
    drives = [chr(x) + ":" for x in range(65, 91) if exists(chr(x) + ":")]
    buttons = [
        Button(drive.upper(), variant="default", classes="tree_button",
               id=f"{drive}_drive")
        for drive in drives
    ]

    buttons = buttons or [Button("/", variant="primary", classes="tree_button",
                                 id="root_drive")]

    def compose(self) -> ComposeResult:
        """Compose the widget."""
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

    def is_system_folder(self, folder_path: Path) -> bool:
        """
        Check if the given folder path belongs to a system folder.

        Args:
            folder_path (Path): The path to the folder.

        Returns:
            bool: True if it's a system folder, False otherwise.
        """
        system_folders = ['$recycle.bin', 'system volume information']
        return any(folder_name.lower() in folder_path.name.lower()
                   for folder_name in system_folders)

    def on_directory_tree_directory_selected(
            self, node: TreeNode[DirEntry]) -> None:
        """
        Event handler when a directory is selected in the DirectoryTree.

        Args:
            node (TreeNode[DirEntry]): The selected node in the tree.
        """
        selected: DirTreeSelected = self.query_one("#dir_selected")
        dir_tree: DirectoryTree = self.query_one("#file_sorter_tree")

        selected_path = node.path

        if not self.is_system_folder(selected_path):
            dir_tree.path = selected.selected = selected_path
            selected.refresh()
            dir_tree.refresh()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler when a button is pressed.

        Args:
            event (Button.Pressed): The button press event.
        """
        up_button: Button = self.query_one("#up_tree")
        selected: DirTreeSelected = self.query_one("#dir_selected")

        if event.button.id.endswith("_drive"):
            drive_letter = str(event.button.label).rstrip(":").lower()
            new_path = f"{drive_letter}:"
            self.cur_dir = Path("/") if new_path == "root" else Path(new_path)
        elif event.button.id == "sort_folder":
            folder_to_sort = self.dir_tree.path
            sorted_file = sorted_folder(folder_to_sort)
            print(f"Sorted folder '{folder_to_sort}' and results saved in "
                  f"'{sorted_file}'")

            self.dir_tree.refresh()
        elif event.button.id == "up_tree":
            self.cur_dir = self.cur_dir.parent
        else:
            return up_button

        self.dir_tree.path = selected.selected = self.cur_dir
        selected.refresh()
        self.dir_tree.refresh()