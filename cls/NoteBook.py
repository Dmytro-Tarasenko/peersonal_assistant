import re
from datetime import datetime

class Note:
    ''' The Class Note is a separate note
    and contains the note_id, content, tags information,
    and several methods for manipulating content and tags.'''    
    
    def __init__(self, content):
        self.note_id = int(datetime.timestamp(datetime.now()))  
        self.content = self._parse_tags(content)  
        self.tags = self._extract_tags(content)  

    def _parse_tags(self, content):
        '''The _parse_tags method removes the tag frame (#) from the text.'''
        return re.sub(r'#(.*?)#', r'\1', content)  

    def _extract_tags(self, content):
        '''The _extract_tags method finds all tags in the text'''
        return re.findall(r'#(.*?)#', content)  

    def edit_note(self, new_content):
        '''The edit_note method re-creates the note content. 
        When editing a note, it parses the new text for tags and selects new tags from the new text.'''
        self.content = self._parse_tags(new_content) 
        self.tags = self._extract_tags(new_content) 

    def __repr__(self):
        '''Showing a note in string form with separators.'''
        return f"{self.note_id}::{'|'.join(self.tags)}::{self.content[:20]}"  
        


class Notebook:

    def __init__(self):
        self.notes = []
        self.tag_pool = {}

    def add_note(self, note_content):
        note = Note(note_content)
        self.notes.append(note)
        self.update_tag_pool(note)
        
    def del_note(self, del_note):
        if del_note in self.notes:
            note_id = del_note.note_id
            self.notes.remove(del_note)
            self.clean_tags(note_id)

    def del_note(self, del_note):
        if del_note in self.notes:
            self.notes.remove(del_note)
            self.clean_tags()

    def find_notes_by_keyword(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower()]
       
    def find_notes_by_tags(self, tag):
	    return [note for note in self.notes if tag.lower() in note.tags]
   
    def update_tag_pool(self, note):
        for tag in note.tags:
            if tag not in self.tag_pool:
                self.tag_pool[tag] = []
            self.tag_pool[tag].append(note.note_id)
    
    def clean_tags(self, note_id):
        tags_to_remove = [tag for tag in self.tag_pool if note_id in self.tag_pool[tag]]
        for tag in tags_to_remove:
            self.tag_pool[tag].remove(note_id)
            if not self.tag_pool[tag]:
                del self.tag_pool[tag]

    def __iter__(self):
        return iter(self.notes)