from PyQt5.QtWidgets import QVBoxLayout, QFrame, QListWidget

from custom_widgets.calendar import PlannerCalendar


class OverviewPanel(QFrame):
    def __init__(self, app, size_widgets: int):
        super().__init__()
        self.app = app

        # Initialize widgets
        self.widget_calendar = PlannerCalendar(self.app)
        self.listwidget_upcoming = QListWidget()

        # Add Widgets to layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.widget_calendar)
        layout.addWidget(self.listwidget_upcoming)

        # Configure Widgets
        self.setup_calendar(int(size_widgets))
        self.setup_upcoming(int(size_widgets))

        self.setLayout(layout)
        self.setObjectName("OverviewPanel")

    def setup_calendar(self, width: int):
        self.widget_calendar.setFixedWidth(width)
        self.widget_calendar.setObjectName("Calendar")

    def setup_upcoming(self, width: int):
        self.listwidget_upcoming.setFixedWidth(width)
        self.listwidget_upcoming.setObjectName("Upcoming")
