from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Button, Header, Footer
from textual import on
from cls.validators import (NameValidator,
                            PhoneNumberValidator,
                            EmailValidator,
                            BirthdayValidator)


class AllInfoValidatorApp(App):
    def action_bell(self):
        self.bell()
    """
        Складає графічний інтерфейс додатка, який містить поля введення 
        для імені, телефону, дня народження та електронної адреси.

        Повертає:
        - ComposeResult: Результат компонування інтерфейсу.
        """
    def compose(self) -> ComposeResult:
        yield Footer()
        yield Header()
        yield Label('Enter user name (only alphabetic'
                    + ' characters|first letter must be capital)')
        yield Input(
            placeholder="Enter user name...",
            validators=[NameValidator()],
            id="name_input",
        )
        yield Label("Enter a user phone number (10 digits):")
        yield Input(
            placeholder="Enter phone number...",
            validators=[PhoneNumberValidator()],
            id="phone_input",
        )
        yield Label("Enter user birthday (in format DD-MM-YYYY)")
        yield Input(
            placeholder="Enter user birthday...",
            validators=[BirthdayValidator()],
            id="birthday_input",
        )
        yield Label("Enter email address (Exa.mple123@email.com)")
        yield Input(
            placeholder="Enter user email...",
            validators=[EmailValidator()],
            id="email_input",
            restrict=None
        )
        yield Button('Submit info')


    @on(Button.Pressed)
    def accept_info(self):
        input_widgets = self.query(Input)

        name_widget = None
        phone_widget = None
        birthday_widget = None
        email_input = None

        validation_errors = []

        for widget in input_widgets:
            validation_result = widget.validate(widget.value)

            if not validation_result.is_valid:
                error_message = validation_result.failure_descriptions[0]
                self.notify(message=error_message,
                            title='Error',
                            severity='error',
                            timeout=7) #Вивід повідомлення
                self.action_bell() #Спрацьовує дзвіночок при помилці
            else:
                if widget.id == "name_input":
                    name_widget = widget.value
                elif widget.id == "phone_input":
                    phone_widget = widget.value
                elif widget.id == "birthday_input":
                    birthday_widget = widget.value
                elif widget.id == "email_input":
                    email_input = widget.value

        def notification():
            if validation_errors:
                for error_message in validation_errors:
                    self.notify(message=error_message,
                                title='Error',
                                severity='error',
                                timeout=7) #Вивід повідомлення
                    self.action_bell() #Спрацьовує дзвіночок при помилці

            if all([name_widget, phone_widget,
                    birthday_widget,email_input]):
                self.notify(message=("User`s information"
                                     + " added to address book"),
                            title="Success",
                            severity="information",
                            timeout=7) #Вивід повідомлення
                for widget in input_widgets:
                    widget.value = ''
        return notification()


if __name__ == "__main__":
    app = AllInfoValidatorApp()
    app.run()
