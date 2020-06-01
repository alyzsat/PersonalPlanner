from course import Course


class DuplicateCourseError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self):
        self._courses = []
        self._hidden_courses = []

    def add_assign_to_course(self, course_name: str, assign_name: str, month: int, day: int):
        index = self.find_index(course_name)
        if index != -1:
            self._courses[index].add_assignment(assign_name, month, day)
        else:
            raise CourseNotFoundError()

    def add_course(self, name: str) -> None:
        index = self.find_index(name)
        if index == -1:
            course = Course(name)
            self._courses.append(course)
        else:
            raise DuplicateCourseError()

    def remove_course(self, name: str) -> None:
        index = self.find_index(name)
        if index != -1:
            self._courses.pop(index)
        else:
            raise CourseNotFoundError()

    def hide_course(self, name: str) -> None:
        index = self.find_index(name)
        if index != -1:
            self._hidden_courses.append(self._courses[index])
        else:
            raise CourseNotFoundError()

    def find_course(self, name: str) -> Course or None:
        index = self.find_index(name)
        if index != -1:
            return self._courses[index]

    def courses(self) -> [Course]:
        return self._courses

    def find_index(self, name: str) -> int:
        for i in range(len(self._courses)):
            if self._courses[i].name() == name:
                return i
        return -1

