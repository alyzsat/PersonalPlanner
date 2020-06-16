from PyQt5.QtWidgets import QLineEdit
from dialogs.dialog import PlannerQDialog


class CourseDialog(PlannerQDialog):
    def __init__(self, app, title: str):
        super().__init__(app, title, 1)
        self.old_name = None

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)

        # Add the widget to dialog
        self.add_widget("Name", self.name_box)

        self.name_box.setFocus()

    def load_info(self, name: str) -> None:
        """Loads the course name to edit course"""
        self.name_box.setText(name)
        self.old_name = name

    def get_info(self) -> str:
        """Return name"""
        return self.name_box.text()

    def ok_clicked(self):
        """Check if course name already exists for creating new course, or
        edit course and change name
        """
        name = self.name_box.text()
        if self.old_name is not None and name.lower() == self.old_name.lower():
            self.accept()
        elif self.app.planner.find_course(name) is None:
            self.accept()
        else:
            self.set_message("Course Already Exists")
