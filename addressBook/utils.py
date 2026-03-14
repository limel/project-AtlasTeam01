# addressBook/utils.py
from datetime import datetime

from .record import Record


def get_phones_str(record):
    return "\n".join(p.value for p in record.phones) if record.phones else "- empty"


def get_emails_str(record):
    return "\n".join(e.value for e in record.emails) if record.emails else "- empty"


def birthday_matches(record, pattern: str) -> bool:
    if not record.birthday or not pattern:
        return False

    bd_part = str(record.birthday)[:5]

    try:
        bd_date = datetime.strptime(bd_part, "%d.%m")
    except ValueError:
        return False

    if "-" not in pattern:
        return pattern in str(record.birthday)

    start_str, end_str = (p.strip() for p in pattern.split("-", 1))

    try:
        start_date = datetime.strptime(start_str, "%d.%m")
        end_date = datetime.strptime(end_str, "%d.%m")
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM-DD.MM")

    if start_date <= end_date:
        return start_date <= bd_date <= end_date

    return bd_date >= start_date or bd_date <= end_date


def record_to_row(record):
    return [
        record.name.value,
        get_phones_str(record),
        get_emails_str(record),
        str(record.birthday) if record.birthday else "- empty",
        record.address.value if record.address else "- empty",
    ]


def match_record(record: Record, field: str, pattern: str) -> bool:
    if field == "name":
        return pattern in record.name.value.lower()
    elif field == "phone":
        return any(pattern in p.value.lower() for p in record.phones)
    elif field == "email":
        return any(pattern in e.value.lower() for e in record.emails)
    elif field == "address":
        addr = record.address.value.lower() if record.address else ""
        return pattern in addr
    elif field == "birthday":
        return birthday_matches(record, pattern)
    return False
