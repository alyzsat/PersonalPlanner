from collections import namedtuple


Date = namedtuple("Date", "month day")


class Assignment:
    def __init__(self, name: str, due_date: Date):
        self._name = name
        self._due_date = due_date
        self._completed = False

    def change_name(self, name: str) -> None:
        self._name = name

    def change_due_date(self, month: int, day: int) -> None:
        self._due_date = Date(month, day)

    def mark_complete(self) -> None:
        self._completed = True

    def mark_incomplete(self) -> None:
        self._completed = False

    def name(self) -> str:
        return self._name

    def due_date(self) -> Date:
        return self._due_date


