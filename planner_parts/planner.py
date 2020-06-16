from planner_parts.assignment import Assignment
from planner_parts.course import Course


class DuplicateCourseError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self):
        self._courses = []
        self._hidden_courses = []
        self._current_course_index = None

    def add_assign(self, course_name: str, assign_name: str, month: int, day: int) -> None:
        """Add an assignment to the given course"""
        self._course_method(course_name, "add_assignment", [assign_name, month, day])

    def remove_assign(self, course_name: str, assign_name: str) -> None:
        """Removes an assignment from the given course"""
        self._course_method(course_name, "remove_assignment", [assign_name])

    def get_assign(self, assign_name: str) -> Assignment:
        """Returns the specified assignment for the current course"""
        return self._courses[self._current_course_index].find_assignment(assign_name)

    def change_course_name(self, course_name: str, new_name: str) -> None:
        """Change the name of the given course"""
        self._course_method(course_name, "change_name", [new_name])

    def add_course(self, name: str) -> None:
        index = self.find_index(name)
        if index == -1:
            course = Course(name)
            if self.is_empty():
                self._current_course_index = 0
            self._courses.append(course)

        else:
            raise DuplicateCourseError()

    def remove_course(self, name: str) -> None:
        index = self.find_index(name)
        if index != -1:
            self._courses.pop(index)
            if self.is_empty():
                self._current_course_index = None
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
            if self._courses[i].name().lower() == name.lower():
                return i
        return -1

    def get_current_course(self) -> Course:
        return self._courses[self._current_course_index]

    def get_current_course_index(self) -> int:
        return self._current_course_index

    def set_current_course(self, name: str) -> None:
        self._current_course_index = self.find_index(name)

    def is_empty(self):
        """Returns True if there are no courses in self._courses
        Ignores self._hidden_courses
        """
        return len(self._courses) == 0

    def _course_method(self, course_name: str, fxn: str, args: list) -> None:
        """Helper function that calls the function (fxn) given
        with the args given on the specified course
        """
        index = self.find_index(course_name)
        if index != -1:
            # Put commas between each argument and put quotation marks
            # around string arguments
            args_string = ", ".join([f"'{arg}'" if (type(arg) == str) else str(arg) for arg in args])
            exec(f"Course.{fxn}(self._courses[{index}], " + args_string + ")")
        else:
            raise CourseNotFoundError()
