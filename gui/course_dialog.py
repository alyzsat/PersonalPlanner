from PyQt5.QtWidgets import QLineEdit, QComboBox
from gui.dialog import PlannerQDialog
from planner import DuplicateCourseError, Planner


class CourseDialog(PlannerQDialog):
    def __init__(self, planner: Planner):
        super().__init__(planner, "Create New Course", 1)

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)

        # Add the widget to dialog
        self.add_widget("Name", self.name_box)

        self.name_box.setFocus()

    def load_info(self, name: str) -> None:
        """Loads the course name to edit course"""
        self.name_box.setText(name)

    def ok_clicked(self):
        """Check if course name already exists"""
        self.set_message("")
        try:
            self.planner.add_course(self.name_box.text())
            self.accept()
        except DuplicateCourseError:
            self.set_message("Course Already Exists")
