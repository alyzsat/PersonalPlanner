from gui.assign_dialog import AssignmentDialog
from gui.course_dialog import CourseDialog
from gui.popup import PlannerPopUp
from planner import Planner, DuplicateCourseError
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QListWidget, QVBoxLayout, QPushButton, QCheckBox, \
    QLabel, QListWidgetItem, QMessageBox, QInputDialog, QDialog, QLineEdit, QComboBox, QGridLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sys


class PersonalPlanner(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.planner = Planner()
        self.test_planner()
        self.layout = QHBoxLayout(self)

        # Setup widgets and Load Planner Details
        # try:
        #     with open("save.txt","r") as file:
        #         file.read()
        # except FileNotFoundError:
        #     with open ("save.txt", "w") as file:
        #         file.write()

        self.current_course_name = "CS 178"
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
        self.planner.courses()[0].add_assignment("Homework 3", 5, 21)
        self.planner.courses()[0].add_assignment("Homework 4", 6, 4)
        self.planner.add_course("CS 190")
        self.planner.courses()[1].add_assignment("Project 1", 4, 28)
        self.planner.courses()[1].add_assignment("Project 2", 5, 27)
        self.planner.add_course("ICS 139W")
        self.planner.courses()[2].add_assignment("Discussion 3", 5, 21)
        self.planner.courses()[2].add_assignment("Proposal Draft", 5, 26)

    def setup_window(self, size: QSize):
        """Set up window dimensions, placement, title, and layout"""
        width = int(size.width() / 2)
        height = int(size.height() / 2)
        x = width - int(width / 2)
        y = height - int(height / 2)
        self.setGeometry(x, y, width, height)
        self.setFixedSize(width, height)
        self.setWindowTitle("Personal Planner")
        self.setWindowIcon(QIcon("logo.png"))
        self.setLayout(self.layout)
        self.setup_sidebar()
        self.setup_assignment_view()
        self.setup_hidden_assignment_view()

    def setup_sidebar(self):
        """Sets up the layout of the side bar"""
        sidebar = QVBoxLayout()
        self.layout.addLayout(sidebar)

        # Course View
        self.refresh_course_view()
        self.course_view.setFixedWidth(int(self.width()/4))
        self.course_view.setCurrentRow(0)
        self.course_view.itemClicked.connect(self.course_clicked)

        # Add Course
        self.add_course_btn.clicked.connect(self.add_course_clicked)

        sidebar.addWidget(self.add_course_btn)
        sidebar.addWidget(self.course_view)

    def setup_assignment_view(self):
        """Creates the layout for the assignment view"""
        assignment_view = QVBoxLayout()
        self.layout.addLayout(assignment_view)

        # Set size with respect to the screen resolution
        self.add_assign_btn.setFixedSize(int(self.width()/7), int(self.height()/16))
        self.course_opt_btn.setFixedSize(int(self.width()/25), int(self.height()/16))

        course_bar = QHBoxLayout()
        course_bar.addWidget(self.current_course)
        course_bar.addWidget(self.add_assign_btn)
        course_bar.addWidget(self.course_opt_btn)

        self.refresh_assign_view()
        self.add_assign_btn.clicked.connect(self.add_assign_clicked)

        assignment_view.addLayout(course_bar)
        assignment_view.addWidget(self.assign_view)

    def setup_hidden_assignment_view(self):
        """Sets up the layout for the hidden assignments"""
        pass

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
        self.refresh_assign_view()

    def add_course_clicked(self):
        """Called when Add Course button is clicked, adds a new Course"""
        dialog = CourseDialog(self.planner)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            self.refresh_course_view()

    def add_assign_clicked(self):
        """Called when Add Assignment button is clicked, adds a
        new assignment to the current course
        """
        dialog = AssignmentDialog(self.planner, self.current_course_name)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            self.refresh_assign_view()

    def test(self, info):
        """Delete this later"""
        print("Testing button", info, self.current_course_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonalPlanner(app.primaryScreen().size())
    sys.exit(app.exec_())
