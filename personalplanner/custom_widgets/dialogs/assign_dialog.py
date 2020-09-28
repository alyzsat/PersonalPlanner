from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLineEdit, QDateEdit, QStyleFactory

from personalplanner.custom_widgets.dialogs.dialog import PlannerQDialog


class AssignmentDialog(PlannerQDialog):
    def __init__(self, app, title: str, assignment_id: int = None):
        super().__init__(app, title, 4)
        self.course = app.planner.get_current_course()
        y, m, d = str(datetime.now().date()).split("-")
        date = QDate(int(y), int(m), int(d))

        # Create Widgets
        self.lineedit_name = QLineEdit()
        self.lineedit_name.textChanged.connect(self.check_text)

        self.dateedit_due = QDateEdit()
        self.dateedit_due.setDate(date)
        self.dateedit_due.setStyle(QStyleFactory.create("Fusion"))

        # Add the Widgets
        self.add_widget("Name", self.lineedit_name)
        self.add_widget("Due Date", self.dateedit_due)

        self.lineedit_name.setFocus()

        self.old_info = None
        if assignment_id is not None:
            self.load_info(assignment_id)

    def get_name(self) -> (str, int, int, str):
        """Return name from QComboBox"""
        return self.lineedit_name.text()

    def get_date(self) -> str:
        """Return the date from QDateEdit as a string, add extra 0 in front
        of single digit months or days
        """
        m, d, y = self.dateedit_due.text().split("/")
        return f"{y}-{0 if len(m) == 1 else ''}{m}-{0 if len(d) == 1 else ''}{d}"

    def load_info(self, assignment_id: int) -> None:
        """Loads assignment information into dialog to edit"""
        self.old_info = self.app.planner.find_assignment(assignment_id)

        _, name, _, _, due_date = self.old_info
        y, m, d = due_date.split("-")
        date = QDate(int(y), int(m), int(d))

        self.lineedit_name.setText(name)
        self.dateedit_due.setDate(date)

    def ok_clicked(self):
        """Attempts to add assignment to course"""
        course_id = self.course[0]
        name = self.get_name()
        date = self.get_date()

        # If the assignment is being edited and the name is the same
        # except with capitalization changes, accept change
        # Also applies for if only the date is being changed
        if len(name) > 25:
            self.set_message(f"25 character limit ({len(name) - 25} chars over)")

        elif len(name) < 3:
            self.set_message("3 character minimum")

        elif self.old_info is not None and name.lower() == self.old_info[1].lower():
            self.app.planner.update_assignment(self.old_info[0], "name", name)
            self.app.planner.update_assignment(self.old_info[0], "due_date", date)
            self.accept()

        # If the assignment name is already being used, set message
        elif self.app.planner.has_assignment(course_id, name):
            self.set_message("Assignment Already Exists")

        # If the assignment is being edited and the name is changed to
        # an available name, update assignment
        elif self.old_info is not None:
            self.app.planner.update_assignment(self.old_info[0], "name", name)
            self.app.planner.update_assignment(self.old_info[0], "due_date", date)
            self.accept()

        # Otherwise, the assignment is new and needs to be added
        else:
            self.app.planner.add_assignment(self.course[0], name, date)
            self.accept()
