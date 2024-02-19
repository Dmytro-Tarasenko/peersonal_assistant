from collections import UserDict
from typing import List, Dict, Set
import re
from datetime import datetime
from interfaces.AbcBook import Book


class Note:
    """ The Class Note is a separate note
    and contains the note_id, content, tags information,
    and several methods for manipulating content and tags."""
    
    def __init__(self,
                 content: str = "",
                 tags: Set[str] | None = None):
        self.note_id: int = int(datetime.timestamp(datetime.now()))
        self.tags = self._extract_tags(content)
        self.tags |= set(tags) if tags else set()
        self.content: str = content.replace("#", "")

    @staticmethod
    def _parse_tags(content: str) -> str:
        """The _parse_tags method checks if the note is empty and removes the tag frame (#) from the text.
        Parameters:
        argument_1(content: str) : It is the string typed by the user
        Returns:
        str:Returning value"""

        if not content:
            raise ValueError('empty_note')
        
        return re.sub(r'#[\w\-]*\b', r'\1', content)

    @staticmethod
    def _extract_tags(content: str) -> Set[str]:
        """The _extract_tags method finds all tags in the text.
        Parameters:
        argument_1(content: str) : It is the string typed by the user.
        Returns:
        List[str]:Returning value"""
        if not content:
            return set()
        res = set()
        for tag in re.findall(r'#[\w\-]*\b', content):
            res |= tag.replace("#", "")

        return res

    def edit_note(self, note_id: int,
                  new_content: str) -> bool:
        """The edit_note method re-creates the note content.
        When editing a note, it parses the new text for tags and selects new tags from the new text."""
        
        # self.content = self._parse_tags(new_content)
        self.tags = self._extract_tags(new_content)
        return True


class Notebook(Book, UserDict[int, Note]):
    """The Class Notebook is a notebook
    and contains a list of notes and dict of tags for quicker searching."""

    def __init__(self) -> None:
        self.tag_pool: Dict[str, List[int]] = {}
        super().__init__()

    def __getitem__(self, item) -> Note | None:
        """
        item - note_id
        """
        for _ in range(self.records_quantity):
            yield self.get_records(_, 1)[0]

    def get_records(self, start: int = 0, limit: int = 5):
        """The get_records method returns a list of notes with the specified range.
        Parameters:
            start (int) : The start of the range.
            limit (int) : The end of the range.
        Returns:
            List[Note]:Returning value"""
        return list(self.data.values())[start:start+limit]

    def add_record(self, note: Note) -> bool:
        """The add_note method creates a new note,
        then adds the note to the list and updates the tag_pool.
        Parameters:
        argument_1(note_content: str) : It's the string typed by the user.
        """
        if _ := self.data.get(note.note_id):
            raise KeyError("note_exists")
        self.data[note.note_id] = note
        Notebook.record_counter += 1
        self._update_tag_pool(note)
        return True
        
    def delete_record(self, del_note: Note) -> None:
        """The del_note method removes a note from the list and clears the tag_pool of unnecessary IDs.
        Parameters:
        argument_1(del_note: Note) : Object of Class Note, note forwarded for deletion.
        """
        if _ := self.data.get(del_note.note_id):
            self._clean_tags(del_note.note_id)
            self.data.pop(del_note.note_id)
            Notebook.record_counter -= 1

    def edit_record(self,
                    old_note: Note,
                    new_note: Note) -> bool:
        pass

    def find_record(self, search_conditions):
        pass

    def iterator(self):
        pass

    def find_notes_by_keyword(self, keywords: List[str]) -> List[Note]:
        """The find_notes_by_keyword method returns a list of notes with the specified keyword in the text.
        Parameters:
        argument_1(keyword: str) : User's request for search.
        Returns:
        List[Note]:Returning value
        """
        res = []
        if len(keywords) == 0 or keywords == [""]:
            return []
        ids_set = set()
        for word in keywords:
            for note in self.data.values():
                if word.lower() in note.content.lower():
                    ids_set |= {note.note_id}
        for note_id in ids_set:
            res.append(self.data.get(note_id))
        return res
       
    def find_notes_by_tags(self, tag: List[str]) -> List[Note]:
        """The find_notes_by_tags method returns a list of notes that have the given tag.
        Parameters:
        argument_1(tag: str) : User's request for search.
        Returns:
        List[Note]:Returning value"""
        if len(tag) == 0 or tag == [""]:
            return []
        res: List[Note] = []
        ids_set = set()
        for entry in tag:
            if id_list := self.tag_pool.get(entry):
                ids_set |= set(id_list)
        for note_id in ids_set:
            res.append(self.data.get(note_id))
        return res
   
    def _update_tag_pool(self, note: Note) -> bool:
        """The _update_tag_pool method adds a new tag if it isn't in the dict
        and adds IDs to the list of the matching tag.
        Parameters:
        argument_1(note: Note) : Object of Class Note, note forwarded for tag_pool updating."""

        for tag in note.tags:
            if tag not in self.tag_pool:
                self.tag_pool[tag] = []
            self.tag_pool[tag].append(note.note_id)

        return True
    
    def _clean_tags(self, note_id: int) -> int:
        """The clean_tags method removes the IDs of a note
        from the list of the matching tag when the note is deleted.
        Parameters:
        argument_1(note_id: int) : value forwarded for deletion note's ID.
        """
        num_removed = 0
        tags_to_remove = [tag for tag in self.tag_pool if note_id in self.tag_pool[tag]]
        for tag in tags_to_remove:
            self.tag_pool[tag].remove(note_id)
            num_removed += 1
            if not self.tag_pool[tag]:
                del self.tag_pool[tag]

        return num_removed
