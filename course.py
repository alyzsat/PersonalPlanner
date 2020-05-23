from assignment import Assignment


class AssignmentNotFoundError(Exception):
    pass


class DuplicateAssignmentError(Exception):
    pass


class Course:
    def __init__(self, name: str):
        self._assignments = []
        self._name = name

    def add_assignment(self, name: str, due_month: int, due_day: int) -> None:
        if self._find_index(name) == -1:
            self._assignments.append(Assignment(name, (due_month, due_day)))
        else:
            raise DuplicateAssignmentError()

    def remove_assignment(self, name: str) -> None:
        index = self._find_index(name)
        if index != -1:
            self._assignments.pop(index)
        else:
            raise AssignmentNotFoundError()

    def find_assignment(self, name: str) -> Assignment or None:
        index = self._find_index(name)
        if index != -1:
            return self._assignments[index]
        else:
            raise AssignmentNotFoundError()

    def clear(self) -> None:
        self._assignments = []

    def assignments(self) -> [Assignment]:
        return self._assignments

    def name(self) -> str:
        return self._name

    def _find_index(self, name: str) -> int:
        for i in range(len(self._assignments)):
            if self._assignments[i].name() == name:
                return i
        return -1
