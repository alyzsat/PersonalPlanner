from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget

from dialogs.course_dialog import CourseDialog
from planner_parts.planner import Planner


class Sidebar(QVBoxLayout):
    def __init__(self, planner: Planner, planner_width: int):
        super().__init__()
        self.planner = planner
        self.setSpacing(20)

        # Initialize widgets
        self.button_add_course = QPushButton()
        self.listwidget_courses = QListWidget()

        # Sizes for widgets
        size_widgets = int(planner_width / 4)

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

    def setup_add_course(self, width: int):
        """Configures the button to add a new course"""
        self.button_add_course.setText("Add Course +")
        self.button_add_course.setFixedWidth(width)
        self.button_add_course.setCursor(Qt.PointingHandCursor)

    def refresh(self):
        """Refreshes the course list view to reflect any changes
        in the list
        """
        courses = [c.name() for c in self.planner.courses()]
        self.listwidget_courses.clear()
        self.listwidget_courses.addItems(courses)
        if not self.planner.is_empty():
            self.listwidget_courses.setCurrentRow(self.planner.get_current_course_index())

    def add_course_clicked(self):
        """Called when the add course button is clicked and opens a
        dialog to add a new course to the planner
        """
        dialog = CourseDialog(self.planner, "Create New Course")
        ok_clicked = dialog.exec_()
        if ok_clicked:
            name = dialog.get_info()
            self.planner.add_course(name)
            self.refresh()
