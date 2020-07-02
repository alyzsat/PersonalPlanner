from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QListWidget, QTableWidget


class OverviewPanel(QFrame):
    def __init__(self, app, planner_width: int):
        super().__init__()
        self.app = app

        # Initialize widgets
        # Not using QCalendarWidget because of styling limitations
        # -> Building a custom calendar from QTableWidget
        self.tablewidget_calendar = QTableWidget()
        self.listwidget_upcoming = QListWidget()

        # Sizes for widgets
        size_widgets = planner_width / 4

        # Add Widgets to layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tablewidget_calendar)
        layout.addWidget(self.listwidget_upcoming)

        # Configure Widgets
        self.setup_calendar(size_widgets)
        self.setup_upcoming(size_widgets)

        self.setLayout(layout)
        self.setObjectName("OverviewPanel")

    def setup_calendar(self, width: int):
        self.tablewidget_calendar.setFixedWidth(width)
        self.tablewidget_calendar.setObjectName("Calendar")

    def setup_upcoming(self, width: int):
        self.listwidget_upcoming.setFixedWidth(width)
        self.listwidget_upcoming.setObjectName("Upcoming")
