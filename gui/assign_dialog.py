from PyQt5.QtWidgets import QLineEdit, QComboBox

from course import DuplicateAssignmentError
from gui.dialog import PlannerQDialog
from planner import Planner


class AssignmentDialog(PlannerQDialog):
    def __init__(self, planner: Planner, course_name: str):
        super().__init__(planner, "Create New Assignment", 3)

        self.course_name = course_name
        months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
        days = [str(i+1) for i in range(31)]

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)
        self.month_box = QComboBox()
        self.month_box.addItems(months)
        self.day_box = QComboBox()
        self.day_box.addItems(days)

        # Add the Widgets
        self.add_widget("Name", self.name_box)
        self.add_widget("Month", self.month_box)
        self.add_widget("Day", self.day_box)

        self.name_box.setFocus()

    def load_info(self, info: list) -> None:
        """Loads assignment information into dialog to edit"""
        name, month, day = info
        self.name_box.setText(name)
        self.month_box.setCurrentIndex(month)
        self.day_box.setCurrentIndex(day)

    def ok_clicked(self):
        """Attempts to add assignment to course"""
        self.set_message("")
        try:
            self.planner.add_assign_to_course(
                self.course_name,
                self.name_box.text(),
                self.month_box.currentIndex(),
                self.day_box.currentIndex())
            self.accept()
        except DuplicateAssignmentError:
            self.set_message("Assignment Already Exists")
