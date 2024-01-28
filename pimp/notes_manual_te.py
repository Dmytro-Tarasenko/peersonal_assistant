from pimp.cls.NoteBook import Note, Notebook
import pickle
from time import sleep

note_book = Notebook()

note = Note(content="Scan through string looking for the first location where the #regular expression #pattern produces a match, and return a corresponding Match. Return None if no position in the string matches the pattern; note that this is different from finding a zero-length match at some point in the string.",
            tags=["python"])
note_book.add_note(note)
sleep(2)

note = Note(content="How to cook borsch? I like #borsch very much. It’s one of the most popular Ukrainian dishes. How to cook borsch? I am going to tell it. To start with",
            tags=["reciept"])
note_book.add_note(note)
sleep(2)
note = Note(content="We're going to build a stopwatch #application. This application should show a list of stopwatches with buttons to start, stop, and reset the stopwatches. We also want the user to be able to add and remove stopwatches as required.",
            tags=["python", "textual", "ui"])

note_book.add_note(note)
sleep(2)
note = Note(content="А́льфа Цента́вра, також #Толіман, Рігіль, Рігіль Центаврус[8] (лат. α Centauri) — найближча до Сонця зоряна система (4,35 світлових років)",
            tags=["astronomy"])

note_book.add_note(note)

with open("data/notebook.bin", "wb") as fout:
    pickle.dump(note_book, fout)

with open("data/notebook.bin", "rb") as fin:
    note_book: Notebook = pickle.load(fin)

print(note_book.find_notes_by_keyword([""]))
print(note_book.find_notes_by_tags([""]))