from errors import BaseError, AddressError, AddressBookError, ErrorHandlerError, SorterError, NoteError, NoteBookError


def error_handler(func):
    """Декоратор обробки помилок і генерації повідомлень про них користувачеві"""

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except AddressError as address_error:
            print(f'Помилка в класі AddressBook: {address_error}')
        except NoteError as note_error:
            print(f'Помилка в класі NoteError: {note_error}')
        except NoteBookError as nb_error:
            print(f'Помилка в класі NoteDookError: {nb_error}')
        except AddressBookError as ab_error:
            print(f'Помилка в класі AddressBookError: {ab_error}')
        except SorterError as sorter_error:
            print(f'Помилка в модулі sorter: {sorter_error}')
        except ErrorHandlerError as err_h_error:
            print(f'Помилка в модулі error_handler: {err_h_error}')
        except BaseError as base_error:
            print(f'Помилка в класі BaseError: {base_error}')
        except Exception as unknown_error:
            print(f'Невідома помилка: {unknown_error}')
        return None
    return wrapper


"""Приклад використання:
class AddressBook:
    @error_handler
    def add_phone(self, phone_number)
        #Логіка додавання номер телефону
        if not self.is_valid(phone_number)
            raise InvalidPhoneError('Ви ввели невалідний номер телефону. Введіть десять цифр без зайвих знаків')
    
    def is_valid(self, phone_number)
        #Логіка перевірки номер телефона на валідність
        return True"""

"""В такому випадку, якщо станеться помилка, вивід буде: 
Помилка в классі AddressBook: Ви ввели невалідний номер телефону. Введіть десять цифр без зайвих знаків

InvalidPhoneError (який наслідується від классу AddresBook) у файлі errors.py пока що не прописан, 
але все вирішуємо поступово, і згодом всі помилки, які в теорії можуть з'явитись будуть додані"""