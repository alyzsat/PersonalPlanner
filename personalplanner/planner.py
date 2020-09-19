import sqlite3
import logging


class DuplicateCourseError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self, data_file: str, date):
        self._data_file = data_file
        self._current_course = None

        logging.basicConfig(filename=f"data/logs/{date.date()}.txt", level=logging.DEBUG)
        self.create_tables(date)
        if not self.is_empty():
            self._current_course = self.courses()[0]

    def create_tables(self, date):
        """Create tables if there is no database created yet"""
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(20),
                    season VARCHAR(10),
                    year INTEGER
                );
                """
            )
            c.execute(
                """CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(40),
                    course_id INTEGER,
                    completed BOOL,
                    due_date DATE,
                    FOREIGN KEY (course_id)
                        REFERENCES courses (id)
                            ON UPDATE NO ACTION
                );
                """
            )
            connection.commit()
            logging.info(f"========== Created tables {str(date.time())} ==========")

        except sqlite3.Error as error:
            logging.error(f"Database Error: {str(error)}")

        finally:
            if connection:
                connection.close()

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

    def get_current_course_index(self) -> int or None:
        courses = self.courses()
        if self._current_course is not None:
            for i in range(len(courses)):
                # If the ID matches the current course's ID
                if courses[i][0] == self._current_course[0]:
                    return i
        return None

    def find_course(self, name: str) -> (int, str, str, int) or None:
        """Returns the information (id, name, season, year) for the course name given
        or None if the course isn't found
        """
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses WHERE name=?", (name, ))
            info = c.fetchone()

        except Exception as e:
            logging.error(f"Planner.find_course: {e}")

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
            c.execute(
                "INSERT INTO courses (name, season, year) VALUES (?, ?, ?)",
                (name.strip(), season, year, )
            )
            connection.commit()
            c.execute("SELECT * FROM courses WHERE name=? AND season=? AND year=?", (name, season, year, ))
            self.set_current_course(c.fetchone())

        except Exception as e:
            logging.error(f"Planner.add_course: {e}")

        finally:
            if connection:
                connection.close()

    def get_course(self, id: int) -> (int, str, str, int):
        """Returns the information (id, name, season, year) for the id given
        or None if the course isn't found
        """
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM courses WHERE id=?", (id, ))
            info = c.fetchone()

        except Exception as e:
            logging.error(f"Planner.get_course: {e}")

        finally:
            if connection:
                connection.close()
            return info

    def update_course(self, course_id: int, field: str, value: str or int) -> None:
        """Given a set of course information, update the details of the course
        with the provided ID
        """
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            query = f"UPDATE courses SET {field}=? WHERE id=?"
            c.execute(query, (value, course_id, ))
            connection.commit()

            if course_id == self.get_current_course()[0]:
                self.set_current_course(self.get_course(course_id))

        except Exception as e:
            logging.error(f"Planner.update_course: {e}")

        finally:
            if connection:
                connection.close()

    def has_course(self, name: str, season: str, year: int) -> bool:
        """Given a set of course information, update the details of the course
        with the provided ID
        """
        connection = None
        course_exists = True
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute(
                "SELECT * FROM courses WHERE name=? AND season=? AND year=? COLLATE NOCASE",
                (name.strip(), season, year, )
            )
            course_exists = len(c.fetchall()) > 0

        except Exception as e:
            logging.error(f"Planner.has_course: {e}")

        finally:
            if connection:
                connection.close()
            return course_exists

    def courses(self, term: (str, int) = None) -> list:
        connection = None
        courses = []
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()

            if term is None:
                c.execute("SELECT * FROM courses")
            else:
                season, year = term
                c.execute("SELECT * FROM courses WHERE season=? and year=?", (season, year, ))
            courses = c.fetchall()

        except Exception as e:
            logging.error(f"Planner.courses: {e}")

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
                c.execute("SELECT * FROM assignments WHERE course_id=? ORDER BY completed, due_date ASC", (course_id, ))
            else:
                c.execute("SELECT * FROM assignments WHERE course_id=? AND completed=0", (course_id, ))
            assignments = c.fetchall()

        except Exception as e:
            logging.error(f"Planner.get_assignments: {e}")

        finally:
            if connection:
                connection.close()
            return assignments

    def add_assignment(self, course_id: int, assignment_name: str, due_date: str) -> None:
        """Adds the assignment to the course with the corresponding id"""
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute(
                "INSERT INTO assignments (name, course_id, completed, due_date) VALUES (?, ?, ?, ?)",
                (assignment_name.strip(), course_id, 0, due_date, )
            )
            connection.commit()

        except Exception as e:
            logging.error(f"Planner.add_assignment: {e}")

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
                (course_id, assignment_name.strip(), )
            )
            assignment_exists = len(c.fetchall()) > 0

        except Exception as e:
            logging.error(f"Planner.has_assignment: {e}")

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

        except Exception as e:
            logging.error(f"Planner.find_assignment: {e}")

        finally:
            if connection:
                connection.close()
            return info

    def delete_assignment(self, assignment_id: int):
        """Delete the assignment from the planner"""
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("DELETE FROM assignments WHERE id=?", (assignment_id, ))
            connection.commit()

        except Exception as e:
            logging.error(f"Planner.delete_assignment: {e}")

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

        except Exception as e:
            logging.error(f"Planner.update_assignment: {e}")

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

        except Exception as e:
            logging.error(f"Planner.size: {e}")

        finally:
            if connection:
                connection.close()
            return size
