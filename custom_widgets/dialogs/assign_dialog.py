from datetime import datetime

from PyQt5.QtWidgets import QLineEdit, QComboBox
from custom_widgets.dialogs.dialog import PlannerQDialog


class AssignmentDialog(PlannerQDialog):
    def __init__(self, app, course: (int, str, str, int), title: str):
        super().__init__(app, title, 4)
        self.course = course

        current_date = datetime.now()
        months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
        days = [str(i + 1) for i in range(31)]
        years = [str(i) for i in range(current_date.year + 2, current_date.year - 5, -1)]

        self.old_name = None
        # Create Widgets
        self.lineedit_name = QLineEdit()
        self.lineedit_name.textChanged.connect(self.check_text)

        self.combobox_month = QComboBox()
        self.combobox_month.addItems(months)
        self.combobox_month.setCurrentIndex(current_date.month - 1)

        self.combobox_day = QComboBox()
        self.combobox_day.addItems(days)
        self.combobox_day.setCurrentIndex(current_date.day - 1)

        self.combobox_year = QComboBox()
        self.combobox_year.addItems(years)
        self.combobox_year.setCurrentIndex(2)

        # Add the Widgets
        self.add_widget("Name", self.lineedit_name)
        self.add_widget("Month", self.combobox_month)
        self.add_widget("Day", self.combobox_day)
        self.add_widget("Year", self.combobox_year)

        self.lineedit_name.setFocus()

    def get_info(self) -> (str, int, int, str):
        """Return name, month, and day from fields"""
        return self.lineedit_name.text(), \
               self.combobox_month.currentIndex() + 1, \
               self.combobox_day.currentIndex() + 1, \
               self.combobox_year.currentText()

    def load_info(self, info: list) -> None:
        """Loads assignment information into dialog to edit"""
        name, month, day, year = info
        self.old_name = name
        self.lineedit_name.setText(name)
        self.combobox_month.setCurrentIndex(month - 1)
        self.combobox_day.setCurrentIndex(day - 1)
        self.combobox_year.setCurrentText(year)

    def ok_clicked(self):
        """Attempts to add assignment to course"""
        name = self.lineedit_name.text()
        course_id = self.course[0]

        # If the assignment is being edited and the name is the same
        # except with capitalization changes, accept change
        if self.old_name is not None and name.lower() == self.old_name.lower():
            self.accept()

        # If the assignment name is already being used, set message
        elif self.app.planner.has_assignment(course_id, name):
            self.set_message("Assignment Already Exists")

        else:
            self.accept()
