from PyQt5.QtWidgets import QLineEdit, QComboBox
from gui.PlannerQDialog import PlannerQDialog


class CourseDialog(PlannerQDialog):
    def __init__(self):
        super().__init__("Create New Course", 1)

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)

        # Add the widget to dialog
        self.add_widget("Name", self.name_box)

    def get_info(self) -> str:
        """Returns a tuple holding the name, month number, and day"""
        return self.name_box.text()

    def load_info(self, name: str) -> None:
        """Loads course name into name box"""
        self.name_box.setText(name)

