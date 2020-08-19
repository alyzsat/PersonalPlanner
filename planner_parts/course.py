from planner_parts.assignment import Assignment


class AssignmentNotFoundError(Exception):
    pass


class DuplicateAssignmentError(Exception):
    pass


class Course:
    def __init__(self, name: str):
        self._assignments = []
        self._name = name

    def add_assignment(self, name: str, due_month: int, due_day: int) -> None:
        if self.has_assignment(name):
            raise DuplicateAssignmentError()
        else:
            self._assignments.append(Assignment(name, (due_month, due_day)))

    def remove_assignment(self, ID: int) -> None:
        index = self._find_index(ID)
        if index != -1:
            self._assignments.pop(index)
        else:
            raise AssignmentNotFoundError()

    def find_assignment(self, ID: int) -> Assignment or None:
        index = self._find_index(ID)
        if index != -1:
            return self._assignments[index]

    def mark_assignment(self, ID: int, status: bool):
        assignment = self.find_assignment(ID)
        assignment.mark_complete(status)

    def has_assignment(self, name: str) -> bool:
        for i in range(len(self._assignments)):
            if self._assignments[i].name().lower() == name.lower():
                return True
        return False

    def clear(self) -> None:
        self._assignments = []

    def assignments(self) -> [Assignment]:
        return self._assignments

    def incomplete_assignments(self) -> [Assignment]:
        return [assign for assign in self._assignments if not assign.is_completed()]

    def name(self) -> str:
        return self._name

    def change_name(self, name: str) -> None:
        self._name = name

    def _find_index(self, ID: int) -> int:
        for i in range(len(self._assignments)):
            if self._assignments[i].get_id() == ID:
                return i
        return -1
