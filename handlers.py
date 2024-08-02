from functools import partial
import error
from address_book import *


add_contact_error = partial(
    error.input_error,
    value_error="Please enter both name and phone number."
)


@add_contact_error
def add_contact(args, book: AddressBook):
    """
    Adds new contact to the contact list

    :param args: expects two arguments - name and phone
    :param book: contacts dictionary
    :return:
    """
    if len(args) < 2:
        raise ValueError

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    return message, False


def exit(args, book: AddressBook):
    """
    Returns goodbye message with the termination flag
    :return:
    """
    return "Good bye!", True


def hello(args, book: AddressBook):
    """
    Returns welcome message
    :return:
    """
    return "How can I help you?", False


set_contact_phone_error = partial(
    error.input_error,
    value_error="Please enter both name and phone number."
)


@set_contact_phone_error
def set_contact_phone(args, book: AddressBook):
    """
    Changes contact phone number if it exists

    :param args: expects two arguments: name and phone
    :param book: contacts dictionary
    :return:
    """
    name, phone = args

    record = book.find(name)
    if record is None:
        raise KeyError

    record.phone = phone

    return "Contacts' phone has been changed.", False


get_contact_phone_error = partial(
    error.input_error,
    value_error="Please enter name to get contact for"
)


@get_contact_phone_error
def get_contact_phone(args, book: AddressBook):
    """
    Returns contact phone number if it exists

    :param args: expects one argument: name
    :param book: contacts dictionary
    :return: contact phone number
    """

    if len(args) == 0:
        raise ValueError

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    return record, False


def get_contacts_list(args, book: AddressBook):
    """
    Returns contacts list as a string

    :param args: doesn't expect any arguments
    :param book: contacts dictionary
    :return: list of contacts in a string representation
    """

    output = ""

    for k, record in book.items():
        phones = []
        for phone in record.phones:
            phones.append(phone.value)

        output += f"{record.name} - {",".join(phones)}\n"

    return output, False


birthday_error = partial(
    error.input_error,
    value_error="Please provide valid birthday date in the following format DD.MM.YYYY.",
    key_error="Record not found for the provided name."
)


@birthday_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError

    record.add_birthday(Birthday(birthday))

    return "Birthday added.", False


@birthday_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError

    if record.birthday is None:
        return "Contact has no birthday.", False

    return record.birthday.value.date(), False


@birthday_error
def birthdays(args, book: AddressBook):
    output = ""

    for bday_info in book.get_upcoming_birthdays():
        output += f"{bday_info["name"]} - {bday_info["congratulation_date"]}\n"

    return output, False


def render_help(commands: dict):
    """
    Renders help message with the commands list
    :param commands:
    :return:
    """
    output = "list of allowed commands: ["

    for command in commands:
        output += f"{command},"

    output = output.strip(',')

    return output + "]"
