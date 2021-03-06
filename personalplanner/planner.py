import sqlite3
import logging
from datetime import datetime


class DuplicateCourseError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class Planner:
    def __init__(self, data_file: str, date):
        self._data_file = data_file
        self._current_course = None
        self._current_term = None

        logging.basicConfig(filename=f"../data/logs/{date.date()}.txt", level=logging.DEBUG)
        self.create_tables(date)

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
        """Sets the currently selected course on the planner

        Params: tuple(id, name, season, year)
        """
        self._current_course = course

    def set_current_term(self, term: (str, int)) -> None:
        """Sets the currently selected course on the planner

        Params: tuple(id, name, season, year)
        """
        self._current_term = term

    def get_current_course(self) -> (int, str, str, int):
        """Returns the currently selected course on the planner in
        the format (id, name, season, year)
        """
        return self._current_course

    def get_current_course_index(self, current_term: (str, int) = None) -> int or None:
        """Get the current course index. If a current term is given, then
        only check the courses for that term
        """
        if current_term is None:
            courses = self.courses()
        else:
            courses = self.courses(current_term)

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
            logging.info(f"{str(datetime.now().time())}: Added course -> name={name}")

        except Exception as e:
            logging.error(f"Planner.add_course: {e}")

        finally:
            if connection:
                connection.close()

    def delete_course(self, id: int) -> None:
        """Permanently delete the course from database"""
        connection = None
        info = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("DELETE FROM courses WHERE id=?", (id,))
            connection.commit()
            logging.info(f"{str(datetime.now().time())}: Deleted course -> id={id}")
            c.execute("DELETE FROM assignments WHERE course_id=?", (id,))
            connection.commit()
            logging.info(f"{str(datetime.now().time())}: -- Deleted corresponding assignments")

            # If current course is being deleted, unset current course
            if id == self._current_course[0]:
                self.set_current_course(None)

        except Exception as e:
            logging.error(f"Planner.delete_course: {e}")

        finally:
            if connection:
                connection.close()
            return info

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
            logging.info(f"{str(datetime.now().time())}: Updated course -> id={course_id}")

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
                c.execute("SELECT * FROM courses ORDER BY id")
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

    def get_assignments_due(self, date: str) -> [(int, str, id, bool, str)]:
        """Returns a list of assignments in the format
        (id: str, name: str, course_name: id, completed: bool, due_date: str)
        for the current course
        """
        assignments = []
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            c.execute("SELECT * FROM assignments WHERE due_date=? ORDER BY due_date ASC", (date, ))
            assignments = c.fetchall()

        except Exception as e:
            logging.error(f"Planner.get_assignments_due: {e}")

        finally:
            if connection:
                connection.close()
            return assignments

    def assignments(self, show_current: bool):
        """Return all incomplete assignments ordered by due date with the closest
        due first
        """
        assignments = []
        connection = None
        try:
            connection = sqlite3.connect(self._data_file)
            c = connection.cursor()
            if show_current:
                c.execute(
                    """
                    SELECT * FROM assignments
                    WHERE course_id IN
                        (SELECT id FROM courses
                        WHERE season=? AND year=?)
                        AND completed=0
                    ORDER BY due_date ASC
                    """,
                    self._current_term
                )
            else:
                c.execute(
                    """
                    SELECT * FROM assignments
                    WHERE completed=0
                    ORDER BY due_date ASC
                    """
                )
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
            logging.info(f"{str(datetime.now().time())}: Add assignment -> name={assignment_name}")

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
            logging.info(f"{str(datetime.now().time())}: Deleted assignment -> id={assignment_id}")

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
            logging.info(f"{str(datetime.now().time())}: Updated assignment -> id={assignment_id}")

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
