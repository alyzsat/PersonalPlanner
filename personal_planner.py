from gui_components.course_page import CoursePage
from gui_components.sidebar import Sidebar
from planner_parts.planner import Planner
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import QSize
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

        self.setup_window(size)

        # Set up GUI components
        self.sidebar = Sidebar(self.planner, self.width())
        self.sidebar.listwidget_courses.itemClicked.connect(self.course_clicked)
        self.sidebar.refresh()

        self.course_page = CoursePage(self.planner, self.width())
        self.course_page.button_course_options.clicked.connect(self.course_options_clicked)
        self.course_page.refresh()

        # Add GUI components
        self.layout.addLayout(self.sidebar)
        self.layout.addLayout(self.course_page)

        self.show()

    def test_planner(self):
        """Temporary values to test out the GUI"""
        self.planner.add_course("CS 178")
        self.planner.add_assign("CS 178", "Homework 3", 5, 21)
        self.planner.add_assign("CS 178", "Homework 4", 6, 4)
        self.planner.add_course("CS 190")
        self.planner.add_assign("CS 190", "Project 1", 4, 28)
        self.planner.add_assign("CS 190", "Project 2", 5, 27)
        self.planner.add_course("ICS 139W")
        self.planner.add_assign("ICS 139W", "Discussion 3", 5, 21)
        self.planner.add_assign("ICS 139W", "Proposal Draft", 5, 26)

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

    # On this module because of interactions outside of SideBar
    def course_clicked(self, item: QListWidgetItem):
        """Called when a course is selected, switches the view
        to display assignments for that course
        """
        self.planner.set_current_course(item.text())
        self.course_page.refresh()

    # On this module because of interactions outside of Course Page
    def course_options_clicked(self):
        """Calls on the course page's function for when the course
        options button is edited. Refreshes the sidebar to reflect changes
        in the name
        """
        self.course_page.course_options_clicked()
        self.sidebar.refresh()

    def test(self, info):
        """Delete this later"""
        print("Testing button", info)
