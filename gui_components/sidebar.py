from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
import logging

from custom_widgets.dialogs.course_dialog import CourseDialog


class Sidebar(QVBoxLayout):
    def __init__(self, app, size_widgets: int):
        super().__init__()
        self.app = app
        self.setSpacing(10)
        self.setContentsMargins(20, 20, 0, 50)

        # Initialize widgets
        self.button_add_course = QPushButton()
        self.listwidget_courses = QListWidget()

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
        self.listwidget_courses.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setup_add_course(self, width: int):
        """Configures the button to add a new course"""
        self.button_add_course.setText("Add Course +")
        self.button_add_course.setFixedWidth(width)
        self.button_add_course.setCursor(Qt.PointingHandCursor)

    def refresh(self):
        """Refreshes the course list view to reflect any changes
        in the list
        """
        self.listwidget_courses.clear()

        if self.app.show_current:
            courses = self.app.planner.courses(self.app.current_term)
        else:
            courses = self.app.planner.courses()

        for id, name, season, year in courses:
            if self.app.show_term_labels:
                label = f"{name}\t({season[:2]} {str(year)[2:]})"
            else:
                label = name
            item = QListWidgetItem()
            item.setData(0, label)  # role 0 is name
            item.setData(1, id)  # role 1 is id
            self.listwidget_courses.addItem(item)

        if not self.app.planner.is_empty():
            index = self.app.planner.get_current_course_index()
            if index is not None:
                self.listwidget_courses.setCurrentRow(index)

        logging.info("Refreshed course list")

    def add_course_clicked(self):
        """Called when the add course button is clicked and opens a
        dialog to add a new course to the planner
        """
        dialog = CourseDialog(self.app, "Create New Course")
        dialog.exec_()
        self.refresh()
