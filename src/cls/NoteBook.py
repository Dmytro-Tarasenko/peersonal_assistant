from collections import UserDict
from typing import List, Dict, Union  # for type annotation
import re  # to search for hashtags using regexp
from datetime import datetime  # to create a unique ID


class Note:
    ''' The Class Note is a separate note
    and contains the note_id, content, tags information,
    and several methods for manipulating content and tags.'''    
    
    def __init__(self,
                 content: str = "",
                 tags: List[str] = []):
        self.note_id: int = int(datetime.timestamp(datetime.now()))  
        self.tags = self._extract_tags(content)
        self.tags.extend(tags)
        self.content: str = content.replace("#", "")

    @staticmethod
    def _parse_tags(content: str) -> str:
        '''The _parse_tags method checks if the note is empty and removes the tag frame (#) from the text.
        Parameters:
        argument_1(content: str) : It is the string typed by the user 
        Returns:
        str:Returning value'''

        if not content:
            raise ValueError('empty_note')
        
        return re.sub(r'#[\w\-]*\b', r'\1', content)

    @staticmethod
    def _extract_tags(content: str) -> List[str]:
        
        '''The _extract_tags method finds all tags in the text.
        Parameters:
        argument_1(content: str) : It is the string typed by the user.
        Returns:
        List[str]:Returning value'''
        if not content:
            return []
        res = []
        for tag in re.findall(r'#[\w\-]*\b', content):
            res.append(tag.replace("#", ""))

        return res

    def edit_note(self, note_id: int,
                  new_content: str) -> None:
        '''The edit_note method re-creates the note content.
        When editing a note, it parses the new text for tags and selects new tags from the new text.'''
        
        # self.content = self._parse_tags(new_content)
        self.tags = self._extract_tags(new_content) 

    def __repr__(self) -> str:

        '''Showing a note in string form with separators.
        Returns:
        str:Returning value'''

        return f"{self.note_id}::{self.content[:50]}::{'|'.join(self.tags)}"
   

class Notebook(UserDict):
    '''The Class Notebook is a notebook 
    and contains a list of notes and dict of tags for quicker searching.'''

    def __init__(self) -> None:
        self.tag_pool: Dict[str, List[int]] = {}
        super().__init__()

    def __getitem__(self, item) -> Note | None:
        """
        item - note_id
        """
        if item in self.data:
            return self.data.get(item)
        return None

    def add_note(self, note: Note) -> None:

        '''The add_note method creates a new note,
        then adds the note to the list and updates the tag_pool.
        Parameters:
        argument_1(note_content: str) : It's the string typed by the user.
        '''
        if _ := self.data.get(note.note_id):
            raise KeyError("note_exists")
        self.data[note.note_id] = note
        self.update_tag_pool(note)
        
    def del_note(self, del_note: Note) -> None:

        '''The del_note method removes a note from the list and clears the tag_pool of unnecessary IDs.
        Parameters:
        argument_1(del_note: Note) : Object of Class Note, note forwarded for deletion. 
        '''
        if _ := self.data.get(del_note.note_id):
            self.clean_tags(del_note.note_id)
            self.data.pop(del_note.note_id)

    def find_notes_by_keyword(self, keywords: List[str]) -> List[Note]:

        '''The find_notes_by_keyword method returns a list of notes with the specified keyword in the text.
        Parameters:
        argument_1(keyword: str) : User's request for search.
        Returns:
        List[Note]:Returning value
        '''
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
        
        '''The find_notes_by_tags method returns a list of notes that have the given tag.
        Parameters:
        argument_1(tag: str) : User's request for search.
        Returns:
        List[Note]:Returning value'''
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
   
    def update_tag_pool(self, note: Note) -> None:

        '''The _update_tag_pool method adds a new tag if it isn't in the dict
        and adds IDs to the list of the matching tag.
        Parameters:
        argument_1(note: Note) : Object of Class Note, note forwarded for tag_pool updating.'''

        for tag in note.tags:
            if tag not in self.tag_pool:
                self.tag_pool[tag] = []
            self.tag_pool[tag].append(note.note_id)
    
    def clean_tags(self, note_id: int) -> None:

        '''The clean_tags method removes the IDs of a note 
        from the list of the matching tag when the note is deleted.
        Parameters:
        argument_1(note_id: int) : value forwarded for deletion note's ID.
        '''

        tags_to_remove = [tag for tag in self.tag_pool if note_id in self.tag_pool[tag]]
        for tag in tags_to_remove:
            self.tag_pool[tag].remove(note_id)
            if not self.tag_pool[tag]:
                del self.tag_pool[tag]
