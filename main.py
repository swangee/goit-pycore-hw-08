import pickle

import handlers
from address_book import *


def parse_input(user_input):
    """
    Parse the input from the user. If there is no input - set default command to "help"
    :param user_input:
    :return:
    """
    if user_input == "":
        return "help", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def main():
    print("Welcome to the assistant bot!")

    # Each handler must accept two arguments: args and contacts dictionary and return tuple with the output
    # and the termination flag if program should exit
    command_to_handler = {
        "close": handlers.exit,
        "exit": handlers.exit,
        "hello": handlers.hello,
        "add": handlers.add_contact,
        "change": handlers.set_contact_phone,
        "phone": handlers.get_contact_phone,
        "add-birthday": handlers.add_birthday,
        "show-birthday": handlers.show_birthday,
        "birthdays": handlers.birthdays,
        "all": handlers.get_contacts_list,
    }

    book = load_data()

    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command == "help":
                print(handlers.render_help(command_to_handler))
                continue

            if command not in command_to_handler:
                print("Invalid command!")
                print(handlers.render_help(command_to_handler))
                continue

            output, should_terminate = command_to_handler[command](args, book)
            print(output)

            if should_terminate:
                break
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
