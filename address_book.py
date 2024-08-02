from datetime import datetime, timedelta
from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.__is_valid(value):
            raise ValueError(f'{value} is not a valid phone number')

        super().__init__(value)

    def __is_valid(self, value: str):
        return bool(re.match(r'^[0-9]{10}$', value))


class Birthday(Field):
    format = '%d.%m.%Y'

    def __init__(self, value):
        try:
            if not self.__is_valid(value):
                raise ValueError

            date = datetime.strptime(value, Birthday.format)

            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __is_valid(self, value: str):
        return bool(re.match(r'^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$', value))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, number: str):
        phones = list(filter(lambda phone: phone.value == number, self.phones))
        if len(phones) == 0:
            return None

        return phones[0]

    def remove_phone(self, number: str):
        phone = self.find_phone(number)
        if phone is not None:
            self.phones.remove(phone)

    def edit_phone(self, number: str, new_number: str):
        phone = self.find_phone(number)
        if phone is not None:
            phone.value = new_number

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name not in self.data:
            return None

        return self.data[name]

    def delete(self, name: str):
        if name not in self.data:
            return

        del self.data[name]

    def get_upcoming_birthdays(self):
        result = []

        today = datetime.today().date()

        for k, record in self.data.items():
            if record.birthday is None:
                continue

            upcoming_birthday = self.__calc_upcoming_birthday_date(today, record.birthday)
            if upcoming_birthday > (today + timedelta(days=7)):
                # Skip users with birthday date later than in a week
                continue

            result.append({"name": record.name, "congratulation_date": self.__calc_congratulation_date(upcoming_birthday)})

        return result

    def __calc_upcoming_birthday_date(self, today, birthday):
        birthday_date = birthday.value.date()

        birthday_this_years = birthday_date.replace(year=today.year)
        congrats_date = birthday_this_years

        if birthday_this_years < today:
            congrats_date = congrats_date.replace(year=today.year+1)

        return congrats_date

    def __calc_congratulation_date(self, upcoming_birthday: datetime.date) -> str:
        congratulation_date = upcoming_birthday
        if congratulation_date.isoweekday() > 5:
            # Move congrats date to the 1st iso weekday (monday) if weekday is saturday or sunday
            congratulation_date = congratulation_date + timedelta(8 - congratulation_date.isoweekday())

        return congratulation_date.strftime(Birthday.format)