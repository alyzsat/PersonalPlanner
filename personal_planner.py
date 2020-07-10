from gui_components.course_page import CoursePage
from gui_components.overview_panel import OverviewPanel
from gui_components.sidebar import Sidebar
from planner_parts.planner import Planner
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from stylesheet_processor import StyleSheetProcessor


class PersonalPlanner(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.planner = Planner()
        self.test_planner()  # ======================== Temporary ========================
        self.layout = QHBoxLayout(self)
        self.setup_window(size)

        # Set up GUI components
        self.sidebar = Sidebar(self, self.width())
        self.sidebar.listwidget_courses.itemClicked.connect(self.course_clicked)
        self.sidebar.button_add_course.clicked.connect(self.add_course_clicked)
        self.sidebar.refresh()

        course_page_width = 11 * self.width() / 20
        self.course_page = CoursePage(self, course_page_width)
        self.course_page.button_course_options.clicked.connect(self.course_options_clicked)
        self.course_page.refresh()

        self.overview_panel = OverviewPanel(self.planner, self.width())

        # Add GUI components
        self.layout.addLayout(self.sidebar)
        self.layout.addWidget(self.course_page)
        self.layout.addStretch()
        self.layout.addWidget(self.overview_panel)

        self.current_theme = "default"
        self.set_theme(self.current_theme, self)

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

        for i in range(1, 5):
            self.planner.add_course("Fake Course #" + str(i))

        for i in range(1, 10):
            self.planner.get_current_course().add_assignment("Fake Assignment #" + str(i), 7, 28)

    def setup_window(self, size: QSize):
        """Set up window dimensions, placement, title, and layout"""
        width = int(size.width() / 2)
        height = int(3 * size.height() / 5)
        x = size.width() / 2 - int(width / 2)
        y = size.height() / 2 - int(height / 2)
        self.setGeometry(x, y, width, height)
        self.setFixedSize(width, height)

        self.setWindowTitle("Personal Planner")
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    # On this module because of interactions outside of SideBar
    def course_clicked(self, item: QListWidgetItem):
        """Called when a course is selected, switches the view
        to display assignments for that course
        """
        self.planner.set_current_course(item.text())
        self.course_page.refresh()

    # On this module because of interactions outside of Side Bar
    def add_course_clicked(self):
        self.sidebar.add_course_clicked()
        self.course_page.refresh()

    # On this module because of interactions outside of Course Page
    def course_options_clicked(self):
        """Calls on the course page's function for when the course
        options button is edited. Refreshes the sidebar to reflect
        changes in the name
        """
        self.course_page.course_options_clicked()
        self.sidebar.refresh()

    def set_theme(self, theme_name: str, widget: QWidget):
        """Runs the StyleSheetProcessor which will replace the
        placeholders in the raw-stylesheet.qss with the attributes
        of the theme, and then sets the stylesheet with the newly
        created stylesheet.qss
        """
        StyleSheetProcessor(theme_name).run()
        with open("assets/stylesheet.qss") as ss:
            widget.setStyleSheet(ss.read())

    def test(self, info):
        # ======================== Temporary ========================
        print("Testing button", info)
