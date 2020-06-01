from gui.assign_dialog import AssignmentDialog
from gui.course_dialog import CourseDialog
from planner import Planner
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QPushButton, QListWidgetItem
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon


class PersonalPlanner(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.planner = Planner()
        self.test_planner()
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)

        # Setup widgets and Load Planner Details
        # try:
        #     with open("save.txt","r") as file:
        #         file.read()
        # except FileNotFoundError:
        #     with open ("save.txt", "w") as file:
        #         file.write()

        with open("assets/stylesheet.qss") as ss:
            self.setStyleSheet(ss.read())

        self.current_course_name = self.planner.courses()[0].name()
        self.current_course = QLabel(self.current_course_name)
        self.add_course_btn = QPushButton("Add Course +")
        self.add_assign_btn = QPushButton("Add Assignment +")
        self.course_opt_btn = QPushButton("•••")
        self.course_view = QListWidget()
        self.assign_view = QListWidget()

        self.setup_window(size)
        self.show()

    def test_planner(self):
        """Temporary values to test out the GUI"""
        self.planner.add_course("CS 178")
        self.planner.add_assign_to_course("CS 178", "Homework 3", 5, 21)
        self.planner.add_assign_to_course("CS 178", "Homework 4", 6, 4)
        self.planner.add_course("CS 190")
        self.planner.add_assign_to_course("CS 190", "Project 1", 4, 28)
        self.planner.add_assign_to_course("CS 190", "Project 2", 5, 27)
        self.planner.add_course("ICS 139W")
        self.planner.add_assign_to_course("ICS 139W", "Discussion 3", 5, 21)
        self.planner.add_assign_to_course("ICS 139W", "Proposal Draft", 5, 26)

    def setup_window(self, size: QSize):
        """Set up window dimensions, placement, title, and layout"""
        width = int(size.width() / 2)
        height = int(size.height() / 2)
        x = width - int(width / 2)
        y = height - int(height / 2)
        self.setGeometry(x, y, width, height)
        self.setFixedSize(width, height)

        self.setWindowTitle("Personal Planner")
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.setLayout(self.layout)
        self.setup_sidebar()
        self.setup_course_page()

    def setup_sidebar(self):
        """Sets up the layout of the left side bar"""
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)
        sidebar.addWidget(self.add_course_btn)
        sidebar.addWidget(self.course_view)
        self.layout.addLayout(sidebar)

        # Course View
        self.course_view.setObjectName("Courses")
        self.refresh_course_view()
        self.course_view.setFixedWidth(int(self.width() / 4))
        self.course_view.setCurrentRow(0)
        self.course_view.itemClicked.connect(self.course_clicked)

        # Add Course
        self.add_course_btn.clicked.connect(self.add_course_clicked)
        self.add_course_btn.setFixedSize(int(self.width() / 4), int(self.height() / 16))
        self.add_course_btn.setCursor(Qt.PointingHandCursor)

    def setup_course_page(self):
        """Creates the layout for the assignment view"""
        course_page = QVBoxLayout()
        course_page.setSpacing(20)
        course_bar = QHBoxLayout()
        course_page.addLayout(course_bar)
        course_page.addWidget(self.assign_view)
        self.layout.addLayout(course_page)

        # Course Description Bar
        self.current_course.setObjectName("CourseNameLabel")
        course_bar.addWidget(self.current_course)
        course_bar.addWidget(self.add_assign_btn)
        course_bar.addWidget(self.course_opt_btn)

        # Add Assignment Button
        self.add_assign_btn.setFixedSize(int(self.width()/5), int(self.height()/16))
        self.add_assign_btn.setCursor(Qt.PointingHandCursor)
        self.add_assign_btn.clicked.connect(self.add_assign_clicked)

        # Course Option Button
        self.course_opt_btn.setFixedSize(int(self.width()/25), int(self.height()/16))
        self.course_opt_btn.setCursor(Qt.PointingHandCursor)
        self.course_opt_btn.clicked.connect(self.course_opt_clicked)

        # Assignment View
        self.assign_view.setObjectName("Assignments")
        self.refresh_assign_view()

    def refresh_assign_view(self):
        """Reloads the assignments to show changes in the assignment list
        or to show assignments for a newly selected course
        """
        assignments = [a.name() for a in self.planner.find_course(self.current_course_name).assignments()]
        self.assign_view.clear()
        self.assign_view.addItems(assignments)

    def refresh_course_view(self):
        """Reloads the courses to show changes in the course list"""
        courses = [c.name() for c in self.planner.courses()]
        self.course_view.clear()
        self.course_view.addItems(courses)

    def course_clicked(self, item: QListWidgetItem):
        """Called when a course is selected, switches the view
        to display assignments for that course
        """
        self.current_course_name = item.text()
        self.current_course.setText(self.current_course_name)
        self.refresh_assign_view()

    def add_course_clicked(self):
        """Called when Add Course button is clicked, adds a new Course"""
        dialog = CourseDialog(self.planner, "Create New Course")
        ok_clicked = dialog.exec_()
        if ok_clicked:
            name = dialog.get_info()
            self.planner.add_course(name)
            self.refresh_course_view()

    def add_assign_clicked(self):
        """Called when Add Assignment button is clicked, adds a
        new assignment to the current course
        """
        dialog = AssignmentDialog(self.planner, self.current_course_name, "Create New Assignment")
        ok_clicked = dialog.exec_()
        if ok_clicked:
            name, month, day = dialog.get_info()
            self.planner.add_assign_to_course(self.current_course_name, name, month, day)
            self.refresh_assign_view()

    def course_opt_clicked(self):
        """Called when the three dots at the top right are clicked
        to edit the course name
        """
        dialog = CourseDialog(self.planner, f"Edit Course: {self.current_course_name}")
        dialog.load_info(self.current_course_name)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            new_name = dialog.get_info()
            self.planner.find_course(self.current_course_name).change_name(new_name)
            self.refresh_course_view()

    def test(self, info):
        """Delete this later"""
        print("Testing button", info, self.current_course_name)
