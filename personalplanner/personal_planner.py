from datetime import datetime

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from personalplanner.settings import Settings
from personalplanner.stylesheet_processor import StyleSheetProcessor
from personalplanner.gui_components.course_page import CoursePage
from personalplanner.gui_components.overview_panel import OverviewPanel
from personalplanner.gui_components.sidebar import Sidebar
from personalplanner.planner import Planner


class PersonalPlanner(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        date = datetime.now()
        self.data_file = "data/planner.db"
        self.config_file = "data/planner.ini"
        self.planner = Planner(self.data_file, date)

        # Settings
        self.settings = Settings(self.config_file)

        self.layout = QHBoxLayout(self)
        self.setup_window(size)

        # GUI components sizes
        sidebar_width = int(self.width() / 6)
        course_page_width = int(self.width() / 2)
        overview_panel_width = int(self.width() / 4)

        # Set up GUI components
        self.sidebar = Sidebar(self, sidebar_width)
        self.sidebar.listwidget_courses.itemClicked.connect(self.course_clicked)
        self.sidebar.button_add_course.clicked.connect(self.add_course_clicked)
        self.sidebar.refresh()
        if not self.planner.is_empty():
            self.sidebar.listwidget_courses.setCurrentRow(0)

        self.course_page = CoursePage(self, course_page_width)
        self.course_page.refresh()

        self.overview_panel = OverviewPanel(self, overview_panel_width)

        # Add GUI components
        # self.layout.addLayout(ToolBar)
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.course_page)
        self.layout.addStretch()
        self.layout.addWidget(self.overview_panel)

        self.set_theme(self.settings.current_theme(), self)
        self.show()

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
        course = self.planner.get_course(item.data(1))
        self.planner.set_current_course(course)
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
        with open("personalplanner/assets/stylesheet.qss") as ss:
            widget.setStyleSheet(ss.read())
            nested = widget.findChild(QWidget, "OverviewPanel")

            if nested is not None:
                self.set_theme_nested(theme_name, nested)

    def set_theme_nested(self, theme_name: str, widget):
        children = widget.findChildren(QWidget)
        for child in children:
            self.set_theme(theme_name, child)
            self.set_theme_nested(theme_name, child)

    def refresh(self):
        self.sidebar.refresh()
        self.course_page.refresh()
        # self.overview_panel.refresh()
