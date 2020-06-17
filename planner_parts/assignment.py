from collections import namedtuple


class Assignment:
    def __init__(self, name: str, due_date: (int, int)):
        self._name = name
        self._due_date = due_date
        self._completed = False

    def __str__(self):
        due_date = f"{self._due_date[0]}/{self._due_date[1]}"
        status = 'Completed' if self._completed else 'Incomplete'
        return f"{self._name}: due {due_date} {status}"

    def change_name(self, name: str) -> None:
        self._name = name

    def change_due_date(self, month: int, day: int) -> None:
        self._due_date = (month, day)

    def mark_complete(self, status: bool) -> None:
        self._completed = status

    def name(self) -> str:
        return self._name

    def due_date(self) -> (int, int):
        return self._due_date

    def is_completed(self) -> bool:
        return self._completed


