from datetime import datetime

from PyQt5.QtWidgets import QLineEdit, QComboBox
from dialogs.dialog import PlannerQDialog


class AssignmentDialog(PlannerQDialog):
    def __init__(self, app, course_name: str, title: str):
        super().__init__(app, title, 3)
        self.course_name = course_name

        months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
        days = [str(i+1) for i in range(31)]
        current_date = datetime.now()

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

        # Add the Widgets
        self.add_widget("Name", self.lineedit_name)
        self.add_widget("Month", self.combobox_month)
        self.add_widget("Day", self.combobox_day)

        self.lineedit_name.setFocus()

    def get_info(self) -> (str, int, int):
        """Return name, month, and day from fields"""
        return self.lineedit_name.text(), self.combobox_month.currentIndex() + 1, self.combobox_day.currentIndex() + 1

    def load_info(self, info: list) -> None:
        """Loads assignment information into dialog to edit"""
        name, month, day = info
        self.old_name = name
        self.lineedit_name.setText(name)
        self.combobox_month.setCurrentIndex(month - 1)
        self.combobox_day.setCurrentIndex(day - 1)

    def ok_clicked(self):
        """Attempts to add assignment to course"""
        name = self.lineedit_name.text()
        if self.old_name is not None and name.lower() == self.old_name.lower():
            self.accept()
        elif self.app.planner.find_course(self.course_name).find_assignment(name) is None:
            self.accept()
        else:
            self.set_message("Assignment Already Exists")
