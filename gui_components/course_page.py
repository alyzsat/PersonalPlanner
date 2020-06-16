from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton

from dialogs.assign_dialog import AssignmentDialog
from dialogs.course_dialog import CourseDialog
from planner_parts.planner import Planner


class CoursePage(QVBoxLayout):
    def __init__(self, planner: Planner, planner_width: int):
        super().__init__()
        self.planner = planner
        self.setSpacing(20)

        # Initialize Widgets
        self.listwidget_assignments = QListWidget()
        self.label_current_course = QLabel()
        self.button_course_options = QPushButton()
        self.button_add_assign = QPushButton()

        # Sizes for Widgets
        size_add_assign = int(planner_width / 5)
        size_course_options = int(planner_width / 20)

        # Create course bar sublayout and add to layout
        course_bar = QHBoxLayout()
        self.addLayout(course_bar)

        # Add Widgets
        course_bar.addWidget(self.label_current_course)
        course_bar.addWidget(self.button_course_options)
        course_bar.addStretch()
        course_bar.addWidget(self.button_add_assign)
        self.addWidget(self.listwidget_assignments)

        # Configure Widgets
        self.setup_assignments()
        self.setup_current_course()
        self.setup_course_options(size_course_options)
        self.setup_add_assignment(size_add_assign)

    def setup_assignments(self) -> None:
        """QListWidget that displays all of the assignments for
        the current course that is selected
        """
        self.listwidget_assignments.setObjectName("Assignments")

    def setup_current_course(self) -> None:
        """Label placed at the top of the window to represent
        the current course to display
        """
        self.label_current_course.setObjectName("LabelCourseName")

    def setup_course_options(self, width: int) -> None:
        """Button that, when clicked, opens a dialog to edit
        the course name
        """
        self.button_course_options.setFixedWidth(width)
        self.button_course_options.setObjectName("CourseOptions")
        self.button_course_options.setText("•••")
        self.button_course_options.setCursor(Qt.PointingHandCursor)

        # Moved connection to PersonalPlanner to be able to refresh the sidebar
        # self.button_course_options.clicked.connect(self.course_options_clicked)

    def setup_add_assignment(self, width: int) -> None:
        """Button that, when clicked, opens a dialog to add
        a new assignment to the current course
        """
        self.button_add_assign.setFixedWidth(width)
        self.button_add_assign.setText("Add Assignment +")
        self.button_add_assign.setCursor(Qt.PointingHandCursor)
        self.button_add_assign.clicked.connect(self.add_assignment_clicked)

    def refresh(self):
        """Refreshes the list of assignments for the current or
        newly selected course. Also changes the course name at
        the top of the page if the course has changed.
        """
        self.listwidget_assignments.clear()
        if self.planner.is_empty():
            self.label_current_course.setText("")
        else:
            self.label_current_course.setText(self.planner.get_current_course().name())
            assignments = [a.name() for a in self.planner.get_current_course().assignments()]
            self.listwidget_assignments.addItems(assignments)

    def course_options_clicked(self):
        """Opens a dialog to edit the course name"""
        current_course_name = self.label_current_course.text()
        dialog = CourseDialog(self.planner, f"Edit Course: {current_course_name}")
        dialog.load_info(current_course_name)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            new_name = dialog.get_info()
            self.planner.change_course_name(current_course_name, new_name)
            self.label_current_course.setText(new_name)

    def add_assignment_clicked(self):
        """Called when Add Assignment button is clicked, adds a
        new assignment to the current course
        """
        current_course_name = self.planner.get_current_course().name()
        dialog = AssignmentDialog(self.planner, current_course_name, "Create New Assignment")
        ok_clicked = dialog.exec_()
        if ok_clicked:
            name, month, day = dialog.get_info()
            self.planner.add_assign(current_course_name, name, month, day)
            self.refresh()