# addressBook/address_book.py
from collections import UserDict
from datetime import datetime, timedelta

from .fields import Birthday
from .record import Record


class AddressBook(UserDict):
    def add_record(self, new_record: Record):
        self.data[str(new_record._id)] = new_record

    def delete(self, record_id: str):
        if record_id in self.data:
            del self.data[record_id]
            return True
        return False

    def find_by_id(self, record_id: str) -> Record | None:
        return self.data.get(record_id)

    def get_upcoming_birthdays(self):
        MAX_DAYS = 7
        today = datetime.today().date()
        max_date = today + timedelta(days=MAX_DAYS)
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue
            bd_this_year = record.birthday.value.replace(year=today.year)
            bd_next_year = record.birthday.value.replace(year=today.year + 1)
            next_bd = bd_next_year if bd_this_year < today else bd_this_year

            if today <= next_bd < max_date:
                # Adjust if birthday falls on weekend
                if next_bd.weekday() in [5, 6]:
                    next_bd += timedelta(days=(7 - next_bd.weekday()))
                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": next_bd.strftime(Birthday.DATE_FORMAT),
                    }
                )

        return upcoming
