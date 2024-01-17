# `GoIT command project - personal_assistant`
![](https://st3.depositphotos.com/3591429/18346/i/450/depositphotos_183464086-stock-illustration-illustration-of-office-worker-avatar.jpg)
## Цей пакет надає функціональність персонального помічника.
### `Назва проекту: “Віртуальний персональний  помічник”`
#### pim - персональний менеджер для щоденних завдань:
*   збереження контактів - імена, адреси, телефон тощо;
*   крнтроль майбутніх днів народжень;
*   ведення особистих нотаток
*   функція сортування файлів в директорії
___
### *Можливості персонального помічника:*
1. зберігає контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
2. перевіряє правильність введеного номера телефону та email під час створення або редагування запису та повідомляє користувача у разі некоректного введення;
3. здійснює пошук контактів серед контактів збережених у книзі;
4. дає можливість редагувати та видаляти записи з книги контактів;
5. виводить список контактів, у яких буде день народження через задану кількість днів від поточної дати;
6. зберігає нотатки з текстовою інформацією;
7. дозволяє проводити пошук за нотатками та додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
8. сортує файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).
___  
### *Технології*

[Textual](https://textual.textualize.io/)

[Rich](https://rich.readthedocs.io/en/stable/index.html)

___

### *Вимоги*
Для встановлення та запуску проекту необхідно:

* [x] linkify-it-py==2.0.2
* [x] markdown-it-py==3.0.0
* [x] mdit-py-plugins==0.4.0
* [x] mdurl==0.1.2
* [x] Pygments==2.17.2
* [x] rich==13.7.0
* [x] textual==0.47.1
* [x] typing_extensions==4.9.0
* [x] uc-micro-py==1.0.2
* [x] ...

___
### *Встановлення:* 
> Як встановити та налаштувати проект?

Ви можете встановити цей пакет за допомогою pip:

```Python
pip install virtual-personal-assistant
```
### *Інтерфейс*
[![image.png](https://i.postimg.cc/SRjJkfVW/image.png)](https://postimg.cc/305KZpsR)
___
### *Використання:* 

> Як використовувати ваш проект? Приклади коду або команд.

`AddressBook` і `Record`  повинні бути імпортовані передвикористанням.

`Sorter` треба додати щось про сортер.

`Note` та `NoteBook` теж стислий опис роботи.

___

#### *Приклади використання додатку*

```Python
# Створення екземпляру помічника
assistant = PersonalAssistant()

# створення контакту
contact = Record(name="John Doe", birthday="25-06-1990", mail="john@example.com")

# Додавання даних до контакту
contact.add_phone("1234567890")
contact.add_edit_address(country="Country", zip_code=12345, city="City", street="Street", house="200", apartment="100")

# створення книги контактів
adress_book = AddressBook()

# Додавання контакту до книги контактів
adress_book.add_record(contact)

# Пошук контакту
result = assistant.find_record("John Doe")

# Створення нотатки
some_note = Note('Content')

# Створення записника
notes_book = Notebook()

# Додавання нотатки
notes_book.add_note(some_note)

# Пошук нотаток за тегами
notes = notes_book.find_notes_by_keyword(keyword)

# і так далі...
```
___

#### Команда проекта:
* [ ] Aleksei Shevchenko
* [ ] Ivan Danyleiko
* [ ] Maksym Skvortsov
* [ ] Angelika Kodlubovska
* [ ] Dmytro Tarasenko
* [ ] Serhii Chabanchuk

___
### Ліцензія:
> #### GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007