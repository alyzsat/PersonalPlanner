from course import Course


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self):
        self._courses = []
        self._hidden_courses = []

    def add_course(self, name: str) -> None:
        # Increase the counter to automatically assign a unique
        # id to each course
        course = Course(name)
        self._courses.append(course)

    def remove_course(self, name: str) -> None:
        index = self._find_index(name)
        if index != -1:
            self._courses.pop(index)
        else:
            raise CourseNotFoundError()

    def hide_course(self, name: str) -> None:
        index = self._find_index(name)
        if index != -1:
            self._hidden_courses.append(self._courses[index])
        else:
            raise CourseNotFoundError()

    def find_course(self, name: str) -> Course or None:
        index = self._find_index(name)
        if index != -1:
            return self._courses[index]
        else:
            raise CourseNotFoundError()

    def courses(self) -> [Course]:
        return self._courses

    def courses_list(self) -> ["Course Names"]:
        return [c.name() for c in self._courses]

    def _find_index(self, name: str) -> int:
        for i in range(len(self._courses)):
            if self._courses[i].name() == name:
                return i
        return -1
