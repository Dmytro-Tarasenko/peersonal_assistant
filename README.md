# GoIT command project - peersonal_assistant
![](https://st3.depositphotos.com/3591429/18346/i/450/depositphotos_183464086-stock-illustration-illustration-of-office-worker-avatar.jpg)
## Цей пакет надає функціональність персонального помічника.
### Назва проекту: “Віртуальний персональний  помічник”
___
## Можливості персонального помічника:
* зберігає контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
* перевіряє правильність введеного номера телефону та email під час створення або редагування запису та повідомляє користувача у разі некоректного введення;
* здійснює пошук контактів серед контактів збережених у книзі;
* дає можливість редагувати та видаляти записи з книги контактів;
* виводить список контактів, у яких буде день народження через задану кількість днів від поточної дати;
* зберігає нотатки з текстовою інформацією;
* дозволяє проводити пошук за нотатками та додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
* сортує файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).
  
### Технології
[Google](http:/google.com)

[Google](http:/google.com)

[Google](http:/google.com) 


### Вимоги
Для встановлення та запуску проекту необхідно:

* [x] вказати, що саме

* [x] ...

### Встановлення: 
> Як встановити та налаштувати проект?

Ви можете встановити цей пакет за допомогою pip:

```Python
pip install virtual-personal-assistant
```




### Використання: 

> Як використовувати ваш проект? Приклади коду або команд.

`AddressBook` і `Record`  повинні бути імпортовані передвикористанням.

`Sorter` треба додати щось про сортер.

`Note` та `NoteBook` теж стислий опис роботи.

```Python
# Створення екземпляру помічника
assistant = AddressBook()

# створення контакту
contact = Record(name="John Doe", birthday="25-06-1990", mail="john@example.com")
contact.add_phone("123-456-7890")
contact.add_edit_address(country="Country", zip_code=12345, city="City",street="Street", house="200", apartment="100")

# Додавання контакту до книги контактів
assistant.add_record(contact)

# Пошук контакту
result = assistant.find_record("John Doe")
print(result)

# Створення нотатки
some_note = Note('Content')

# Створення записника
notes_book = Notebook()


# Додавання нотатки
notes_book.add_note(some_note)

# Пошук нотаток за тегами
notes = notes_book.find_notes_by_keyword(keyword)
print(notes)

# і так далі...
```
#### Команда проекта:
* Aleksei Shevchenko
* Ivan Danyleiko
* Maksym Skvortsov
* Angelika Kodlubovska
* Dmytro Tarasenko
* Serhii Chabanchuk


### Ліцензія: 
> #### GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
