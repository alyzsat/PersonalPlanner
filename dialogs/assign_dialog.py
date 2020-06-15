from datetime import datetime

from PyQt5.QtWidgets import QLineEdit, QComboBox
from dialogs.dialog import PlannerQDialog
from planner_parts.planner import Planner


class AssignmentDialog(PlannerQDialog):
    def __init__(self, planner: Planner, course_name: str, title: str):
        super().__init__(planner, title, 3)
        self.course_name = course_name

        months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
        days = [str(i+1) for i in range(31)]
        current_date = datetime.now()

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)

        self.month_box = QComboBox()
        self.month_box.addItems(months)
        self.month_box.setCurrentIndex(current_date.month - 1)

        self.day_box = QComboBox()
        self.day_box.addItems(days)
        self.day_box.setCurrentIndex(current_date.day - 1)

        # Add the Widgets
        self.add_widget("Name", self.name_box)
        self.add_widget("Month", self.month_box)
        self.add_widget("Day", self.day_box)

        self.name_box.setFocus()

    def get_info(self) -> (str, int, int):
        """Return name, month, and day from fields"""
        return self.name_box.text(), self.month_box.currentIndex() + 1, self.day_box.currentIndex() + 1

    def load_info(self, info: list) -> None:
        """Loads assignment information into dialog to edit"""
        name, month, day = info
        self.name_box.setText(name)
        self.month_box.setCurrentIndex(month - 1)
        self.day_box.setCurrentIndex(day - 1)

    def ok_clicked(self):
        """Attempts to add assignment to course"""
        self.set_message("")
        if self.planner.find_course(self.course_name).find_assignment(self.name_box.text()) is None:
            self.accept()
        else:
            self.set_message("Assignment Already Exists")
