import sqlite3


class DuplicateCourseError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self, data_file: str, config_file: str):
        self._data_file = data_file
        self._config_file = config_file
        self._current_course = None
        if not self.is_empty():
            self._current_course = self.courses()[0]

    def data_file(self):
        """Returns the path to the data file"""
        return self._data_file

    def set_current_course(self, course: (int, str, str, int)) -> None:
        """Sets the currently selected course on the planner"""
        self._current_course = course

    def get_current_course(self) -> (int, str, str, int):
        """Returns the currently selected course on the planner in
        the format (id, name, season, year)
        """
        return self._current_course

    def get_current_course_index(self) -> int:
        courses = self.courses()
        if self._current_course is not None:
            for i in range(len(courses)):
                # If the ID matches the current course's ID
                if courses[i][0] == self._current_course[0]:
                    return i
        return None

    def find_course(self, id: int) -> (int, str, str, int) or None:
        """Returns the information (id, name, season, year) for the course name given
        or None if the course isn't found
        """
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses WHERE id=?", (id, ))
            info = c.fetchone()

        except sqlite3.Error as e:
            print("Planner.find_course:", e)

        finally:
            if connection:
                connection.close()
            return info

    def add_course(self, name: str, season: str, year: int) -> None:
        """Adds a course to the planner database"""
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("INSERT INTO courses (name, season, year) VALUES (?, ?, ?)", (name, season, year, ))
            connection.commit()
            c.execute("SELECT * FROM courses WHERE name=? AND season=? AND year=?", (name, season, year, ))
            self.set_current_course(c.fetchone())

        except sqlite3.Error as e:
            print("Planner.add_course", e)

        finally:
            if connection:
                connection.close()

    def update_course(self, course_info: (int, str, str, int)) -> None:
        """Given a set of course information, update the details of the course
        with the provided ID
        """
        id, name, season, year = course_info
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("UPDATE courses SET name=?, season=?, year=? WHERE id=?", (name, season, year, id, ))
            connection.commit()

        except sqlite3.Error as e:
            print("Planner.update_course", e)

        finally:
            if connection:
                connection.close()

    def has_course(self, name: str, season: str, year: int) -> None:
        """Given a set of course information, update the details of the course
        with the provided ID
        """
        connection = None
        course_exists = True
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses WHERE name=? AND season=? AND year=? COLLATE NOCASE", (name, season, year, ))
            course_exists = len(c.fetchall()) > 0

        except sqlite3.Error as e:
            print("Planner.has_course", e)

        finally:
            if connection:
                connection.close()
            return course_exists

    def courses(self) -> list:
        connection = None
        courses = []
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses")
            courses = c.fetchall()

        except sqlite3.Error as e:
            print("Planner.courses:", e)

        finally:
            if connection:
                connection.close()
            return courses

    def get_assignments(self, course_id: int, show_completed: bool) -> [(int, str, str, bool, str)]:
        """Returns a list of assignments in the format
        (id: str, name: str, course_name: str, completed: bool, due_date: str)
        for the current course
        """
        assignments = []
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            if show_completed:
                c.execute("SELECT * FROM assignments WHERE course_id=? ORDER BY completed", (course_id, ))
            else:
                c.execute("SELECT * FROM assignments WHERE course_id=? AND completed=0", (course_id, ))
            assignments = c.fetchall()

        except sqlite3.Error as e:
            print("Planner.get_assignments:", e)

        finally:
            if connection:
                connection.close()
            return assignments

    def add_assignment(self, course_id: int, assignment_name: str, month: int, day: int, year: str) -> None:
        """Adds the assignment to the course with the corresponding id"""
        connection = None
        try:
            due_date = f"{year}-{month}-{day}"
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute(
                "INSERT INTO assignments (name, course_id, completed, due_date) VALUES (?, ?, ?, ?)",
                (assignment_name, course_id, 0, due_date, )
            )
            connection.commit()

        except sqlite3.Error as e:
            print("Planner.add_assignment:", e)

        finally:
            if connection:
                connection.close()

    def has_assignment(self, course_id: int, assignment_name: str) -> bool:
        """Returns true if an assignment with that name exists for the given course"""
        """Adds the assignment to the course with the corresponding id"""
        connection = None
        assignment_exists = True
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute(
                "SELECT * FROM assignments WHERE course_id=? AND name=? COLLATE NOCASE",
                (course_id, assignment_name, )
            )
            assignment_exists = len(c.fetchall()) > 0

        except sqlite3.Error as e:
            print("Planner.has_assignment:", e)

        finally:
            if connection:
                connection.close()
            return assignment_exists

    def find_assignment(self, assignment_id: int):
        """Return assignment details"""
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM assignments WHERE id=?", (assignment_id, ))
            info = c.fetchone()

        except sqlite3.Error as e:
            print("Planner.update_assignment:", e)

        finally:
            if connection:
                connection.close()
            return info

    def update_assignment(self, assignment_id: int, field: str, value) -> None:
        """Update whether or not the assignment has been completed"""
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            query = f"UPDATE assignments SET {field}=? WHERE id=?"
            c.execute(query, (value, assignment_id, ))
            connection.commit()

        except sqlite3.Error as e:
            print("Planner.update_assignment:", e)

        finally:
            if connection:
                connection.close()

    def is_empty(self):
        """Returns True if planner has no courses"""
        return self.size() == 0

    def size(self):
        """Returns the number of courses in the planner"""
        connection = None
        size = 0
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses")
            courses = c.fetchall()
            size = len(courses)

        except sqlite3.Error as e:
            print("Planner.size:", e)

        finally:
            if connection:
                connection.close()
            return size

    # ==============================================================================

    def remove_assign(self, course_name: str, assign_id: int) -> None:
        """Removes an assignment from the given course"""
        self._course_method(course_name, "remove_assignment", [assign_id])

    def change_course_name(self, course_name: str, new_name: str) -> None:
        """Change the name of the given course"""
        self._course_method(course_name, "change_name", [new_name])

    def remove_course(self, name: str) -> None:
        index = self.find_index(name)
        if index != -1:
            self._courses.pop(index)
            if self.is_empty():
                self._current_course_index = None
        else:
            raise CourseNotFoundError()

    def get_index(self, name: str) -> int:
        for i in range(len(self._courses)):
            if self._courses[i].name().lower() == name.lower():
                return i
        return -1

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
