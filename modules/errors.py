class BaseError(Exception):
    """Базовий клас для помилок у модулі error_handler.py"""

    def __init__(self, message="Помилка в модулі error_handler"):
        self.message = message
        super().__init__(self.message)


class AddressBookError(BaseError):
    """Помилка, пов'язана з класом AddressBook"""
    pass


class NoteBookError(BaseError):
    """Помилка, пов'язана з класом NoteBook"""
    pass


class NoteError(BaseError):
    """Помилка, пов'язана з класом Note"""
    pass


class AddressError(BaseError):
    """Помилка, пов'язана з класом Address"""
    pass


class SorterError(BaseError):
    """Помилка, пов'язана з модулем sorter"""
    pass


class ErrorHandlerError(BaseError):
    """Помилка, пов'яазана з модулем error_handler"""
    pass
