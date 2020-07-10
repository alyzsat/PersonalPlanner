from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget

from dialogs.course_dialog import CourseDialog
from dialogs.popup import PlannerPopUp


class Sidebar(QVBoxLayout):
    def __init__(self, app, planner_width: int):
        super().__init__()
        self.app = app
        self.setSpacing(20)
        self.setContentsMargins(20, 20, 0, 50)

        # Initialize widgets
        self.button_add_course = QPushButton()
        self.listwidget_courses = QListWidget()

        # Sizes for widgets
        size_widgets = int(planner_width / 5)

        # Add Widgets to layout
        self.addWidget(self.button_add_course)
        self.addWidget(self.listwidget_courses)

        # Configure Widgets
        self.setup_add_course(size_widgets)
        self.setup_courses(size_widgets)

    def setup_courses(self, width: int):
        """Configures the QListWidget for holding courses"""
        self.listwidget_courses.setObjectName("Courses")
        self.listwidget_courses.setFixedWidth(width)
        self.listwidget_courses.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setup_add_course(self, width: int):
        """Configures the button to add a new course"""
        self.button_add_course.setText("Add Course +")
        self.button_add_course.setFixedWidth(width)
        self.button_add_course.setCursor(Qt.PointingHandCursor)

    def refresh(self):
        """Refreshes the course list view to reflect any changes
        in the list
        """
        courses = [c.name() for c in self.app.planner.courses()]
        self.listwidget_courses.clear()
        self.listwidget_courses.addItems(courses)
        if not self.app.planner.is_empty():
            self.listwidget_courses.setCurrentRow(self.app.planner.get_current_course_index())

    def add_course_clicked(self):
        """Called when the add course button is clicked and opens a
        dialog to add a new course to the planner
        """
        if len(self.app.planner.courses()) == 8:
            PlannerPopUp(self.app, "Error", "Max course count reached (8)").show()
        else:
            dialog = CourseDialog(self.app, "Create New Course")
            ok_clicked = dialog.exec_()
            if ok_clicked:
                name = dialog.get_info()
                self.app.planner.add_course(name)
                self.app.planner.set_current_course(name)
                self.refresh()
